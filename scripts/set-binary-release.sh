#!/usr/bin/env bash
# Points a Package.swift at a release's prebuilt XCFrameworks.
#
#   set-binary-release.sh <Package.swift> <version> <dir with *.xcframework.zip.sha256>
#
# Replaces the manifest's one `let binaryRelease ... = nil` line with the version and a
# checksum per module. Run by the release workflow on the commit it tags; the result is
# never committed to a branch.
set -euo pipefail

manifest="$1"
version="$2"
dist="$3"
unset_line='let binaryRelease: (version: String, checksums: [String: String])? = nil'

[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "Bad version: $version" >&2; exit 1; }
[[ "$(grep -cFx "$unset_line" "$manifest")" == 1 ]] || {
    echo "$manifest: expected exactly one unset binaryRelease line" >&2
    exit 1
}

entries=()
for file in "$dist"/*.xcframework.zip.sha256; do
    [[ -e "$file" ]] || { echo "No checksums in $dist" >&2; exit 1; }
    module="$(basename "$file" .xcframework.zip.sha256)"
    checksum="$(tr -d '[:space:]' < "$file")"
    [[ "$checksum" =~ ^[0-9a-f]{64}$ ]] || { echo "Bad checksum for $module" >&2; exit 1; }
    entries+=("\"$module\": \"$checksum\"")
done
joined="$(IFS=,; echo "${entries[*]}")"
replacement="let binaryRelease: (version: String, checksums: [String: String])? = (\"$version\", [${joined//,/, }])"

awk -v from="$unset_line" -v to="$replacement" '$0 == from { print to; next } { print }' \
    "$manifest" > "$manifest.tmp"
mv "$manifest.tmp" "$manifest"
