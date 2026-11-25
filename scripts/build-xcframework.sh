#!/usr/bin/env bash
# Builds <Module>.xcframework.zip and its SwiftPM checksum from a Swift package.
#
#   build-xcframework.sh <package dir> <output dir> <module> [<module> ...]
#
# One dynamic framework per module, one slice per platform the package declares
# (device and simulator), with the Swift interface and the module's resource bundle.
# The package's manifest must make its library products dynamic when
# PV_XCFRAMEWORK_BUILD is set; see docs/xcframework-releases.md.
#
# Modules are built in the order given. Each finished one is left in
# <package dir>/.xcframework-build and named in PV_XCFRAMEWORK_PREBUILT, so a manifest
# can hand it to the modules after it as a binary target. List a module after the
# modules it imports, or their code is linked into it a second time.
#
# Each module is compiled under its own package name: Swift will not load a prebuilt
# module that claims the package of the code importing it. `package` access therefore
# cannot cross modules in a released package.
set -euo pipefail

package_dir="$(cd "$1" && pwd)"
mkdir -p "$2"
output="$(cd "$2" && pwd)"
shift 2
modules=("$@")
[[ ${#modules[@]} -gt 0 ]] || { echo "No modules given" >&2; exit 1; }

cd "$package_dir"
export PV_XCFRAMEWORK_BUILD=1
manifest="$(xcrun swift package dump-package)"
package_name="$(jq -r .name <<<"$manifest")"

destinations=()
while read -r platform; do
    case "$platform" in
        ios) destinations+=('iOS' 'iOS Simulator') ;;
        tvos) destinations+=('tvOS' 'tvOS Simulator') ;;
        watchos) destinations+=('watchOS' 'watchOS Simulator') ;;
        visionos) destinations+=('visionOS' 'visionOS Simulator') ;;
        macos) destinations+=('macOS') ;;
        maccatalyst) destinations+=('macOS,variant=Mac Catalyst') ;;
        *) echo "Unknown platform in manifest: $platform" >&2; exit 1 ;;
    esac
done < <(jq -r '.platforms[].platformName' <<<"$manifest")
# PV_XCFRAMEWORK_PLATFORMS narrows the list for a quick local check, e.g. "iOS Simulator".
if [[ -n "${PV_XCFRAMEWORK_PLATFORMS:-}" ]]; then
    IFS='|' read -r -a destinations <<<"$PV_XCFRAMEWORK_PLATFORMS"
fi

scratch="$(mktemp -d)"
prebuilt_dir="$package_dir/.xcframework-build"
rm -rf "$prebuilt_dir"
trap 'rm -rf "$scratch" "$prebuilt_dir"' EXIT
export PV_XCFRAMEWORK_PREBUILT=""

for module in "${modules[@]}"; do
    framework_args=()
    for platform in "${destinations[@]}"; do
        slice="$scratch/$module/${platform//[^a-zA-Z]/_}"
        xcodebuild archive -quiet -scheme "$module" \
            -destination "generic/platform=$platform" \
            -archivePath "$slice/archive" -derivedDataPath "$slice/derived" \
            -skipPackagePluginValidation -skipMacroValidation \
            SKIP_INSTALL=NO BUILD_LIBRARY_FOR_DISTRIBUTION=YES CODE_SIGNING_ALLOWED=NO \
            SWIFT_PACKAGE_NAME="${module}_xcframework"

        framework="$(find "$slice/archive.xcarchive/Products" -name "$module.framework" -print -quit)"
        products="$slice/derived/Build/Intermediates.noindex/ArchiveIntermediates/$module/BuildProductsPath"
        swiftmodule="$(find "$products" -name "$module.swiftmodule" -type d -print -quit)"
        bundle="$(find "$products" -name "${package_name}_$module.bundle" -print -quit)"
        [[ -n "$framework" && -n "$swiftmodule" ]] || {
            echo "Missing framework or Swift module for $module on $platform" >&2
            exit 1
        }
        [[ -n "$(find "$swiftmodule" -name '*.swiftinterface' -print -quit)" ]] || {
            echo "No Swift interface for $module on $platform" >&2
            exit 1
        }

        # macOS frameworks are versioned; everything goes under Versions/Current.
        root="$framework"
        resources="$framework"
        if [[ -d "$framework/Versions/Current" ]]; then
            root="$framework/Versions/Current"
            resources="$root/Resources"
            ln -s Versions/Current/Modules "$framework/Modules"
        fi
        mkdir -p "$root/Modules"
        ditto "$swiftmodule" "$root/Modules/$module.swiftmodule"
        # Bundle.module looks for <package>_<target>.bundle beside the code that asks.
        if [[ -n "$bundle" ]]; then
            mkdir -p "$resources"
            ditto "$bundle" "$resources/${package_name}_$module.bundle"
        fi
        framework_args+=(-framework "$framework")
        rm -rf "$slice/derived"
    done

    xcodebuild -create-xcframework "${framework_args[@]}" -output "$scratch/$module.xcframework"
    ditto -c -k --norsrc --noextattr --keepParent "$scratch/$module.xcframework" "$output/$module.xcframework.zip"
    xcrun swift package compute-checksum "$output/$module.xcframework.zip" > "$output/$module.xcframework.zip.sha256"
    echo "$module: $(cat "$output/$module.xcframework.zip.sha256")"

    mkdir -p "$prebuilt_dir"
    ditto "$scratch/$module.xcframework" "$prebuilt_dir/$module.xcframework"
    PV_XCFRAMEWORK_PREBUILT="${PV_XCFRAMEWORK_PREBUILT:+$PV_XCFRAMEWORK_PREBUILT }$module"
done
