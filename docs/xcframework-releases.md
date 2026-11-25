# Prebuilt XCFramework releases for the shared packages

The Swift packages Provenance, iFly and iCube share
([list](https://wiki.provenance-emu.com/help/shared-frameworks)) ship as prebuilt
XCFrameworks. An app that depends on a version tag compiles none of the package.

## The rule

- **A version tag is binary.** The tagged `Package.swift` has `binaryRelease` set, and
  every module is a `binaryTarget` pointing at `<Module>.xcframework.zip` in that tag's
  GitHub Release, by checksum.
- **A branch is source.** `binaryRelease` is `nil` on `main` and every other branch, so a
  dependency by branch or revision builds from source and can never pick up a stale binary.
- **`PV_BUILD_FROM_SOURCE=1` forces source** for a tagged version. Set it in the
  environment `xcodebuild` (or Xcode) starts in, then resolve packages again.

The tagged commit differs from the commit it was built from by one line of
`Package.swift`, and sits on no branch.

## Releasing

Run **Release XCFramework** from the package's Actions tab with the new version
(`dry_run` builds and checks without tagging). Each package's `release.yml` calls
[`release-xcframework.yml`](../.github/workflows/release-xcframework.yml) here, which:

1. builds one dynamic framework per module and per platform the manifest declares
   ([`scripts/build-xcframework.sh`](../scripts/build-xcframework.sh)), with the Swift
   interface and the module's resource bundle inside;
2. writes the version and checksums into `Package.swift`
   ([`scripts/set-binary-release.sh`](../scripts/set-binary-release.sh)), commits, tags
   that commit and pushes the tag;
3. creates the GitHub Release with the zips.

Never push a version tag by hand: it has no binary and builds from source.

To check a package locally:

```bash
PV_XCFRAMEWORK_PLATFORMS='iOS Simulator' scripts/build-xcframework.sh ../PVSystems dist PVSystems
```

## What a package's manifest needs

```swift
let binaryRelease: (version: String, checksums: [String: String])? = nil

let environment = ProcessInfo.processInfo.environment
let buildFromSource = binaryRelease == nil || environment["PV_BUILD_FROM_SOURCE"] != nil
let libraryType: Product.Library.LibraryType? = environment["PV_XCFRAMEWORK_BUILD"] != nil ? .dynamic : nil
```

- The `binaryRelease` line must appear exactly as above; the release script replaces it.
- Each released module has a library product of the same name, of type
  `buildFromSource ? libraryType : nil`.
- `targets:` is `buildFromSource ? sourceTargets : binaryTargets`. Product names are the
  same in both modes, so consumers change nothing.

## Rules for the code

- **Every public enum is `@frozen`.** The frameworks are built with library evolution, and
  in the Swift 6 language mode a `switch` over a non-frozen enum from such a framework
  does not compile without `@unknown default`. Apps pin an exact version and rebuild
  against it, so frozen is true in practice.
- **No type named after its module** in new packages; it breaks qualified names in Swift
  interfaces.

## Packages with several modules or dependencies

- List `modules` in dependency order. The build script leaves each finished framework in
  `.xcframework-build/` and names it in `PV_XCFRAMEWORK_PREBUILT`; the manifest turns a
  named module into a `binaryTarget(path:)`, so the next module links it instead of
  compiling it in a second time. PVRemoteLibrary's `Package.swift` is the model.
- A target names every package its imports' interfaces import, not only its own imports:
  a prebuilt framework does not pass its dependencies on.
- A binary target cannot declare dependencies. In a release, an empty source target
  (`Sources/BinaryDependencies`) carries the packages the frameworks link against, and
  each product lists it.
- A dependency on another shared package must be on a version that has a binary release,
  or its code is linked into the framework statically.
- `package` access cannot cross modules: each framework is compiled under its own
  package name, because Swift will not load a prebuilt module that claims the importing
  code's package.

## Not converted yet

Packages that depend on another package need their dependencies to be binary first, or
the dependency is linked into the framework a second time:

- on another shared package: PVRemoteLibrary, PVCloudSync, PVContinuity;
- on third-party packages (ZIPFoundation, SQLite.swift, swift-crypto): PVLookup,
  ContinuityKit, SkinKit (which publishes XCFrameworks but still resolves from source);
- several modules that depend on each other: GamepadKit, PVWidgets, PVPatchEngine (C core).

PVWebServer follows the same rule with its own script and a single-checksum
`binaryRelease`.
