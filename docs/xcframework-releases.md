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

1. builds one dynamic framework per module and per platform the manifest declares (plus
   Mac Catalyst whenever iOS is declared)
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

## Which Xcode builds a release

Xcode 26.3, the oldest Xcode the apps build with. A `.swiftinterface` loads in the
compiler that wrote it or a newer one; Xcode 27 writes module selectors (`Module::Type`)
that Xcode 26 cannot read. The first releases cut by this workflow (PVSystems 1.0.2,
PVSyncRules 1.0.3, PVHelp 1.0.1, PVLibrarySnapshot 1.0.1, PVWebServer 1.3.4) were built
with Xcode 27 and are superseded; do not pin them.

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

## State of each package

Binary from these versions on: PVSystems 1.0.3, PVSyncRules 1.0.4, PVLibrarySnapshot 1.0.2,
PVHelp 1.0.2, PVWebServer 1.3.5, PVPatchEngine 1.0.2, PVRemoteLibrary 0.3.1,
PVCloudSync 1.1.1, PVContinuity 1.0.1, ContinuityKit 1.0.2, PVLookup 1.1.0, SkinKit 0.8.0.
GamepadKit has the manifest and workflow but no binary release yet.

Still source: **PVWidgets.** Its widget configuration intent does not survive a Swift
interface: the `@Parameter` property wrapper is printed without its arguments and fails
to compile.

## Third-party libraries

A library that several modules use, or that the apps use too, comes from
[PVDependencies](https://github.com/Provenance-Emu/PVDependencies): prebuilt SQLite.swift
and ZIPFoundation, one copy for the app and every package. PVLookup and SkinKit depend
on it, in source mode as well.

- **One source per library.** A graph cannot hold PVDependencies' `ZIPFoundation` and the
  upstream package at once (two modules of one name). An app that uses PVLookup or
  SkinKit takes these libraries from PVDependencies too.
- **A library used by one module** may instead be an `internal import`, linked inside
  that module's framework and absent from its interface: Lighter and swift-crypto in
  PVLookup, ZIPFoundation in ContinuityKit. It must compile with library evolution,
  because the whole build does (Lighter needed 1.0.1 for that).
- **Helpers shared between a package's modules** are `@_spi(<Package>) public`, not
  `package`: see PVLookup.

## Keeping the apps and the wiki current

Nothing has to be bumped by hand after a release:

- **Apps.** Each app has an `update-shared-packages.yml` workflow (hourly, and by hand). It
  runs [`scripts/bump-shared-packages.py`](../scripts/bump-shared-packages.py), which raises
  every Provenance-Emu package the app names to its latest released version, in manifests,
  Xcode package references and lock files, and opens or updates one pull request
  (`deps/shared-packages`). A new major version is listed in the PR, not applied.
- **Wiki.** `sync-shared-frameworks.yml` in the wiki repo regenerates the
  [Shared Frameworks](https://wiki.provenance-emu.com/help/shared-frameworks) page from the
  package repositories.

Both poll, so they need no cross-repository token. A pull request opened with the default
Actions token does not start other workflows; set a `SHARED_PACKAGES_TOKEN` secret (a
token that may push and open pull requests) in an app repository to get CI on those PRs.
