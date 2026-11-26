#!/usr/bin/env python3
"""Move an app onto the latest release of each shared Provenance-Emu package.

Run in an app's checkout. For every github.com/Provenance-Emu package the app's
manifests name, finds the highest major.minor.patch tag that has a GitHub release and,
where the app asks for less, raises:

- version requirements in Package.swift / Project.swift (`from:`, `.upToNextMajor`,
  `.upToNextMinor`, `exact`), on the line that names the package;
- `minimumVersion` of Xcode package references in project.pbxproj;
- pins in Package.resolved / .package.resolved (version and revision).

A new major version is reported, not applied. Revision and branch pins are left alone.
Writes a Markdown summary to the path in --summary (for a pull request body) and prints
`changed=true|false` for GitHub Actions.

    GH_TOKEN=$(gh auth token) python3 bump-shared-packages.py [--summary FILE] [--only Name]
"""
import argparse
import json
import os
import re
import subprocess
import urllib.error
import urllib.request

OWNER = "Provenance-Emu"
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
PACKAGE = re.compile(r"github\.com/" + OWNER + r"/([A-Za-z0-9_-]+?)(?:\.git)?[\"/]")
REQUIREMENT = re.compile(r"((?:from:|exact:|\.exact\()\s*\")(\d+\.\d+\.\d+)(\")")
MANIFESTS = ("Package.swift", "Project.swift")
LOCKS = ("Package.resolved", ".package.resolved")


def api(path):
    request = urllib.request.Request(f"https://api.github.com/{path}")
    request.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        request.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def key(version):
    return tuple(int(part) for part in SEMVER.match(version).groups())


def latest(name, cache={}):
    """(version, commit sha) of the newest released version, or None."""
    if name not in cache:
        releases = [r["tag_name"] for r in api(f"repos/{OWNER}/{name}/releases?per_page=100") or []
                    if SEMVER.match(r["tag_name"]) and not r["draft"] and not r["prerelease"]]
        cache[name] = None
        if releases:
            version = max(releases, key=key)
            cache[name] = (version, api(f"repos/{OWNER}/{name}/commits/{version}")["sha"])
    return cache[name]


def tracked(names):
    files = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout.split("\n")
    # A sparse checkout lists files it does not have.
    return [f for f in files if f and os.path.basename(f) in names and os.path.isfile(f)]


def newer(current, target):
    """True when target is a later version of the same major."""
    return key(target) > key(current) and key(target)[0] == key(current)[0]


def bump_manifest(path, only, log):
    lines = open(path).read().split("\n")
    changed = False
    for index, line in enumerate(lines):
        found = PACKAGE.search(line)
        if not found or (only and found.group(1) != only):
            continue
        name, release = found.group(1), latest(found.group(1))
        requirement = REQUIREMENT.search(line)
        if not release or not requirement:
            continue
        current = requirement.group(2)
        if newer(current, release[0]):
            lines[index] = line[:requirement.start(2)] + release[0] + line[requirement.end(2):]
            log.setdefault(name, set()).add((current, release[0]))
            changed = True
        elif key(release[0])[0] > key(current)[0]:
            log.setdefault("major", set()).add((name, current, release[0]))
    if changed:
        open(path, "w").write("\n".join(lines))
    return changed


def bump_pbxproj(path, only, log):
    text = open(path).read()
    block = re.compile(r"(repositoryURL = \"[^\"]*github\.com/" + OWNER + r"/([A-Za-z0-9_-]+?)(?:\.git)?\";"
                       r"\s*requirement = \{[^}]*?minimumVersion = )(\d+\.\d+\.\d+)(;)", re.S)

    def replace(match):
        name, current, release = match.group(2), match.group(3), latest(match.group(2))
        if (only and name != only) or not release or not newer(current, release[0]):
            return match.group(0)
        log.setdefault(name, set()).add((current, release[0]))
        return match.group(1) + release[0] + match.group(4)

    updated = block.sub(replace, text)
    if updated != text:
        open(path, "w").write(updated)
    return updated != text


def bump_lock(path, only, log):
    text = open(path).read()
    try:
        pins = json.loads(text).get("pins", [])
    except ValueError:
        return False
    updated = text
    for pin in pins:
        found = PACKAGE.search(pin.get("location", "") + "\"")
        state = pin.get("state", {})
        if not found or "version" not in state or (only and found.group(1) != only):
            continue
        name, release = found.group(1), latest(found.group(1))
        if not release or not SEMVER.match(state["version"]) or not newer(state["version"], release[0]):
            continue
        block = re.search(r"\{[^{}]*\"location\" : \"" + re.escape(pin["location"]) + r"\"[^{}]*\{[^{}]*\}[^{}]*\}",
                          updated, re.S)
        if not block:
            continue
        replaced = (block.group(0).replace(state["revision"], release[1])
                    .replace(f"\"version\" : \"{state['version']}\"", f"\"version\" : \"{release[0]}\""))
        updated = updated.replace(block.group(0), replaced)
        log.setdefault(name, set()).add((state["version"], release[0]))
    if updated != text:
        open(path, "w").write(updated)
    return updated != text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary")
    parser.add_argument("--only", help="bump this package only")
    arguments = parser.parse_args()

    log, files = {}, []
    for path in tracked(MANIFESTS):
        if bump_manifest(path, arguments.only, log):
            files.append(path)
    for path in tracked(("project.pbxproj",)):
        if bump_pbxproj(path, arguments.only, log):
            files.append(path)
    for path in tracked(LOCKS):
        if bump_lock(path, arguments.only, log):
            files.append(path)

    majors = sorted(log.pop("major", set()))
    rows = []
    for name in sorted(log):
        target = max((new for _, new in log[name]), key=key)
        olds = ", ".join(sorted({old for old, _ in log[name]}, key=key))
        rows.append(f"| [{name}](https://github.com/{OWNER}/{name}) | {olds} | "
                    f"[{target}](https://github.com/{OWNER}/{name}/releases/tag/{target}) |")
    summary = []
    if rows:
        summary += ["| Package | From | To |", "|---|---|---|", *rows, "",
                    f"{len(files)} files changed. Lock files were edited by this script, not resolved by "
                    "Xcode or Tuist, so their `originHash` may be stale; the next resolve rewrites it.", ""]
    if majors:
        summary += ["New major versions, not applied (they may break the API):", ""]
        summary += [f"- {name}: {current} → {target}" for name, current, target in majors] + [""]
    if arguments.summary:
        open(arguments.summary, "w").write("\n".join(summary))
    print("\n".join(summary))
    print(f"changed={'true' if files else 'false'}")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as output:
            output.write(f"changed={'true' if files else 'false'}\n")
            output.write("packages=" + ", ".join(f"{n} {max((x for _, x in log[n]), key=key)}" for n in sorted(log)) + "\n")


if __name__ == "__main__":
    main()
