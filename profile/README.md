<div align="center">

<img src="https://provenance-emu.com/img/logo.png" alt="Provenance" width="280">

### The Premier Open-Source Multi-System Emulator for iPhone, iPad & Apple TV

[![App Store](https://img.shields.io/badge/App_Store-Free-0D96F6?style=flat-square&logo=apple&logoColor=white)](https://apps.apple.com/us/app/provenance-app/id1596862805)
[![GitHub Stars](https://img.shields.io/github/stars/Provenance-Emu/Provenance?style=flat-square&logo=github&color=FA3399)](https://github.com/Provenance-Emu/Provenance/stargazers)
[![Discord](https://img.shields.io/discord/421819941761728512?style=flat-square&logo=discord&logoColor=white&label=Discord&color=5865F2)](https://discord.gg/4TK7PU5)
[![License](https://img.shields.io/badge/License-Provenance-8000CC?style=flat-square)](https://github.com/Provenance-Emu/Provenance/blob/develop/LICENSE.md)

</div>

---

## What Is Provenance?

Provenance is a free, open-source multi-system emulator that brings **38+ classic gaming systems** to iPhone, iPad, and Apple TV — with native iOS features, beautiful artwork, and 10+ years of active development.

```
No jailbreak. No ads. No tracking. Just your games.
```

**[→ Get it on the App Store](https://apps.apple.com/us/app/provenance-app/id1596862805)**
**[→ AltStore / Sideload](https://provenance-emu.com/install/)**
**[→ Build from Source](https://wiki.provenance-emu.com/installation-and-usage/installing-provenance/building-from-source)**

---

## Supported Systems

<table>
<tr>
<td valign="top">

**Nintendo**
- Game Boy / Color / Advance
- NES / Famicom / FDS
- SNES / Super Famicom
- Nintendo 64 / 64DD
- Nintendo DS · 3DS
- GameCube · Wii
- Virtual Boy · Pokémon Mini

</td>
<td valign="top">

**Sega**
- Master System · SG-1000
- Genesis / Mega Drive
- Sega CD · 32X
- Game Gear · Saturn
- Dreamcast

</td>
<td valign="top">

**Sony & NEC**
- PlayStation (PS1)
- PlayStation 2 ⚠️ (Play! — requires JIT)
- PlayStation Portable
- PC Engine / TurboGrafx-16
- PC Engine CD · SuperGrafx
- PC-FX

</td>
<td valign="top">

**Atari, SNK & More**
- Atari 2600 · 5200 · 7800 · Lynx
- Atari Jaguar · Jaguar CD
- Neo Geo · Pocket · Pocket Color
- WonderSwan · Color
- 3DO · Intellivision · Vectrex
- ColecoVision · Odyssey 2
- And more…

</td>
</tr>
</table>

[View the full system compatibility list →](https://wiki.provenance-emu.com/info/supported-systems)

---

## Key Features

| Feature | Details |
|---------|---------|
| 🎨 **Custom Skins** | Full support for `.deltaskin` / `.manicskin` controller layouts — [browse the catalog](https://provenance-emu.com/skins/) |
| 🏆 **RetroAchievements** | Unlock achievements across 100+ supported systems |
| 💾 **iCloud Sync** | Save states, game library, and skins sync across all your devices |
| 🕹️ **Controller Support** | MFi, Xbox, PlayStation, Siri Remote, and keyboard |
| 🎮 **Cheat Codes** | In-app lookup from the libretro database across 12+ cores |
| 📺 **Apple TV / tvOS** | Full tvOS support with TopShelf integration |
| 🖼️ **Artwork & Metadata** | Automatic box art, screenshots, ratings, and manuals |
| 🌀 **CRT Shaders** | 7 built-in Metal filters including Simple CRT, Complex CRT, VHS, LCD, Game Boy |
| 📦 **CHD Support** | Native CHD disc image support across CD-based cores |
| 🔓 **100% Free** | Open source, no ads, no tracking — forever |

---

## Repositories

### Core Project
| Repo | Description |
|------|-------------|
| [Provenance](https://github.com/Provenance-Emu/Provenance) | Main iOS/tvOS app — Swift, UIKit, SwiftUI |
| [iCube](https://github.com/Provenance-Emu/iCube) | GameCube and Wii emulator for iPhone, iPad and Apple TV at [icube-emu.com](https://icube-emu.com) |
| [emulator-content-server](https://github.com/Provenance-Emu/emulator-content-server) | Headless library server for ROMs, saves, artwork and BIOS |
| [wiki](https://github.com/Provenance-Emu/wiki) | Documentation at [wiki.provenance-emu.com](https://wiki.provenance-emu.com) |
| [skins](https://github.com/Provenance-Emu/skins) | Community skin catalog at [provenance-emu.com/skins](https://provenance-emu.com/skins/) |
| [provenance-emu.github.io](https://github.com/Provenance-Emu/provenance-emu.github.io) | Main website at [provenance-emu.com](https://provenance-emu.com) |

### Shared Swift Packages

The parts Provenance, [iFly](https://ifly-emu.com) and [iCube](https://icube-emu.com) have in common, each a standalone Swift package any emulator frontend can use. Version tags resolve to prebuilt XCFrameworks. [Developer docs →](https://wiki.provenance-emu.com/help/shared-frameworks)

| Package | What it does | Used by | Platforms | Latest |
|---------|--------------|---------|-----------|--------|
| [SkinKit](https://github.com/Provenance-Emu/SkinKit) | Controller skins: `.deltaskin` / `.manicskin` parsing, the Format 2 renderer, the skin manager and store browser, RetroArch overlay import, and the TV bezels around the picture (`SkinKitBezels`). | Provenance, iFly, iCube | iOS 17, tvOS 17, macOS 14 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/SkinKit?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [GamepadKit](https://github.com/Provenance-Emu/GamepadKit) | Controller handling: element-name mapping, positional fallback for plain HID pads, pad family detection, pause triggers, and a synthesized extended gamepad for pads iOS exposes without one (Switch Online SNES / N64 / Mega Drive, generic USB and Bluetooth pads). | Adoption in progress (`0.1.0`) | iOS 17.4, tvOS 17.4, macOS 14 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/GamepadKit?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [PVSystems](https://github.com/Provenance-Emu/PVSystems) | `SystemIdentifier` and per-system metadata: TheGamesDB / libretrodb / OpenVGDB IDs, RetroAchievements console IDs, the per-game BIOS manifest. | Provenance, iFly | iOS 17, tvOS 17, macOS 14, watchOS 9, visionOS 1 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/PVSystems?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [PVLookup](https://github.com/Provenance-Emu/PVLookup) | Game metadata, artwork and cheat lookup over libretrodb, OpenVGDB, TheGamesDB, ShiraGame and the libretro cheat database. Ships no database bytes; they are release assets fetched at build time. | Provenance, iFly | iOS 17, tvOS 17, macOS 14, watchOS 9, visionOS 1 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/PVLookup?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [PVPatchEngine](https://github.com/Provenance-Emu/PVPatchEngine) | Streaming ROM and disc patch engine: IPS, BPS, UPS, PPF and xdelta3, with bounded memory and 64-bit offsets. C core, Swift API. | Provenance, iFly, iCube | iOS 17, tvOS 17, macOS 14 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/PVPatchEngine?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [PVWebServer](https://github.com/Provenance-Emu/PVWebServer) | HTTP and WebDAV server on one port, built on Network.framework, with a route registry. Powers the in-app file manager and uploads. | Provenance, iCube | iOS 17, tvOS 17, macOS 11, watchOS 9, visionOS 1 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/PVWebServer?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [PVWidgets](https://github.com/Provenance-Emu/PVWidgets) | Home screen game widgets: grid and list drawn from the widget's real size, the Show and Layout options, cover decoding. | Provenance, iFly, iCube | iOS 17, tvOS 17, macOS 14, visionOS 1 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/PVWidgets?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [PVLibrarySnapshot](https://github.com/Provenance-Emu/PVLibrarySnapshot) | The App Group snapshot and cover JPEGs an app writes for its extensions; the tvOS Top Shelf reads it. | Provenance, iCube | iOS 17, tvOS 17, macOS 14, visionOS 1 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/PVLibrarySnapshot?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [PVHelp](https://github.com/Provenance-Emu/PVHelp) | In-app help from a GitBook wiki repo: navigation, page fetch and cache, GitBook preprocessing, offline fallback. | Provenance, iCube | iOS 17, tvOS 17, macOS 14, watchOS 9, visionOS 1 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/PVHelp?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [PVRemoteLibrary](https://github.com/Provenance-Emu/PVRemoteLibrary) | One model of "a game somewhere": on this device, on an emulator content server, on a RomM share or on a nearby peer. Matching, merged library rows, an on-disk catalogue and cover cache. | Provenance | iOS 17, tvOS 17, macOS 14, visionOS 1 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/PVRemoteLibrary?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [PVSyncRules](https://github.com/Provenance-Emu/PVSyncRules) | What an emulator app syncs: `SyncClassifier` (save state, battery save, ROM, BIOS), `SyncableFileType`, `SyncPolicy`. Pure value types, no I/O. | iCube | iOS 17, tvOS 17, macOS 14 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/PVSyncRules?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [PVCloudSync](https://github.com/Provenance-Emu/PVCloudSync) | CloudKit sync of user files: scanning, planning, conflict resolution, tombstones, a local trash, retry policy and a CloudKit provider. | iCube | iOS 17, tvOS 17, macOS 14 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/PVCloudSync?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [PVContinuity](https://github.com/Provenance-Emu/PVContinuity) | Nearby library discovery, trust, manifests and file transfer between devices on the same network. | iCube | iOS 17, tvOS 17, macOS 14 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/PVContinuity?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [ContinuityKit](https://github.com/Provenance-Emu/ContinuityKit) | Cross-device "continue this game" handoff: manifests, transfer, Bonjour discovery, library browse. A different API and wire protocol from PVContinuity. | iFly | iOS 16, tvOS 16, macOS 13, watchOS 9, visionOS 1 | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/ContinuityKit?style=flat-square&label=&color=8000CC&filter=!databases-*&sort=semver) |
| [PVDependencies](https://github.com/Provenance-Emu/PVDependencies) | Prebuilt XCFrameworks of the third-party libraries the apps and packages share (SQLite.swift, ZIPFoundation): one copy per app, never compiled. | Provenance, iFly, iCube | iOS, tvOS, macOS, watchOS, visionOS | ![tag](https://img.shields.io/github/v/tag/Provenance-Emu/PVDependencies?style=flat-square&label=&color=8000CC&sort=semver) |

### Languages

| Language | What we write in it | Where |
|----------|---------------------|-------|
| Swift | The apps, SwiftUI and UIKit interfaces, every shared package, widgets, App Intents, build tools | [Provenance](https://github.com/Provenance-Emu/Provenance), [iCube](https://github.com/Provenance-Emu/iCube), all shared packages |
| Objective-C / Objective-C++ | The bridge between Swift and each emulator core, controller input mapping | [Provenance](https://github.com/Provenance-Emu/Provenance) `Cores/`, [Core-VirtualJaguar](https://github.com/Provenance-Emu/Core-VirtualJaguar) |
| C / C++ | Emulator core forks and patches (Dolphin, Azahar, Virtual Jaguar, Flycast), the libretro frontend, the patch engine | [iCube](https://github.com/Provenance-Emu/iCube), [PVPatchEngine](https://github.com/Provenance-Emu/PVPatchEngine), [Provenance](https://github.com/Provenance-Emu/Provenance) |
| Metal Shading Language / GLSL | CRT, LCD and VHS video filters, the slang shader runtime | [Provenance](https://github.com/Provenance-Emu/Provenance) `PVShaders` |
| TypeScript | The library server and its clients, the iCube and iFly websites (Next.js) | [emulator-content-server](https://github.com/Provenance-Emu/emulator-content-server), [icube-emu.github.io](https://github.com/Provenance-Emu/icube-emu.github.io), [ifly-emu.github.io](https://github.com/Provenance-Emu/ifly-emu.github.io) |
| Svelte | The library server web interface | [emulator-content-server](https://github.com/Provenance-Emu/emulator-content-server) |
| Rust | Parts of the library server | [emulator-content-server](https://github.com/Provenance-Emu/emulator-content-server) |
| Python | The skin catalog pipeline, database generators, build and maintenance scripts | [skins](https://github.com/Provenance-Emu/skins), [PVLookup](https://github.com/Provenance-Emu/PVLookup), [Provenance](https://github.com/Provenance-Emu/Provenance) `Scripts/` |
| Shell | Build, release and XCFramework packaging scripts | every repo |
| Ruby | fastlane lanes, the Homebrew cask | [Provenance](https://github.com/Provenance-Emu/Provenance), [homebrew-virtualjaguar](https://github.com/Provenance-Emu/homebrew-virtualjaguar) |
| CMake / Make | Native core builds for iOS and tvOS | [Provenance](https://github.com/Provenance-Emu/Provenance), [iCube](https://github.com/Provenance-Emu/iCube) |
| HTML / CSS / SCSS / JavaScript | The websites (Hugo), the in-app file manager page | [provenance-emu.github.io](https://github.com/Provenance-Emu/provenance-emu.github.io), [PVWebServer](https://github.com/Provenance-Emu/PVWebServer) |

### Emulation Cores
| Repo | System(s) |
|------|-----------|
| [Core-Mednafen](https://github.com/Provenance-Emu/Core-Mednafen) | PS1, PC Engine, Virtual Boy, Lynx, WonderSwan, NGP |
| [Core-PPSSPP](https://github.com/Provenance-Emu/Core-PPSSPP) | PlayStation Portable |
| [Core-Gambatte](https://github.com/Provenance-Emu/Core-Gambatte) | Game Boy / Color |
| [Core-VisualBoyAdvance](https://github.com/Provenance-Emu/Core-VisualBoyAdvance) | Game Boy Advance |
| [Core-SNES9x](https://github.com/Provenance-Emu/Core-SNES9x) | Super Nintendo |
| [Core-FCEUX](https://github.com/Provenance-Emu/Core-FCEUX) | NES / Famicom |
| [Core-Mupen64Plus](https://github.com/Provenance-Emu/Core-Mupen64Plus) | Nintendo 64 |
| [Core-Gen-Plus-GX](https://github.com/Provenance-Emu/Core-Gen-Plus-GX) | Sega Genesis, Master System, Game Gear |
| [Core-Stella](https://github.com/Provenance-Emu/Core-Stella) | Atari 2600 |
| [Core-VirtualJaguar](https://github.com/Provenance-Emu/Core-VirtualJaguar) | Atari Jaguar |
| [Core-ProSystem](https://github.com/Provenance-Emu/Core-ProSystem) | Atari 7800 |
| [Core-PicoDrive](https://github.com/Provenance-Emu/Core-PicoDrive) | Sega 32X, Mega CD |
| [Core-PokeMini](https://github.com/Provenance-Emu/Core-PokeMini) | Pokémon Mini |
| [Core-Atari800](https://github.com/Provenance-Emu/Core-Atari800) | Atari 8-bit |

---

## Contributing

Contributions are welcome across all our repos:

- 🐛 **Bug reports** → [GitHub Issues](https://github.com/Provenance-Emu/Provenance/issues)
- 🎨 **Submit a skin** → [provenance-emu.com/skins/submit.html](https://provenance-emu.com/skins/submit.html)
- 📝 **Improve the wiki** → [github.com/Provenance-Emu/wiki](https://github.com/Provenance-Emu/wiki)
- 💻 **Code contributions** → Fork the [main repo](https://github.com/Provenance-Emu/Provenance) and open a PR against `develop`

---

## Community

<div align="center">

[![Discord](https://img.shields.io/badge/Join_Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/4TK7PU5)
[![Twitter/X](https://img.shields.io/badge/Follow_@ProvenanceApp-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/provenanceapp)
[![App Store](https://img.shields.io/badge/Rate_on_App_Store-0D96F6?style=for-the-badge&logo=apple&logoColor=white)](https://apps.apple.com/us/app/provenance-app/id1596862805)

</div>

---

## Members

- [Joe Mattiello](https://github.com/JoeMatt) — Lead Developer
- [James Addyman](https://github.com/jasarien) — Co-founder

---

<div align="center">
<sub>Built with ❤️ since 2016 · <a href="https://provenance-emu.com">provenance-emu.com</a></sub>
</div>
