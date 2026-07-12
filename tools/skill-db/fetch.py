#!/usr/bin/env python3
"""Build skills.json: global skill names + base costs + gold/white prereq pairs.

Usage:
    python3 fetch.py            # refresh skills.json from the network

Sources (kachi-dev/uma-tools — the umalator's own repo, global-aligned):
  - skill_meta.json (master branch): per skill ID -> baseCost, groupId, iconId.
  - deployed umalator-global bundle.js: embeds an id -> official global English
    name map, covering only skills released on the global version.

Pairing rules (verified against in-game Learn screens):
  - trainable skills (6-digit 2xxxxx ids): within a groupId, id ending 1 is the
    upgrade (rare gold, or ◎ for green stat skills) and id ending 2 is its
    prereq (white / ○). Suffix 3 is the × variant (not purchasable upward).
  - green families also have a suffix-4 member: the rare gold (e.g. Firm Course
    Menace). Its Learn-screen bundle stacks the whole chain ○ -> ◎ -> gold, so
    it is recorded with pair = the ○ and middle = the ◎.
  - a name appearing under both a 1xxxxx id (someone's unique, baseCost 0) and
    a 9xxxxx id (the purchasable inherited version) resolves to the 9xxxxx id.
"""
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

META_URL = "https://raw.githubusercontent.com/kachi-dev/uma-tools/master/skill_meta.json"
BUNDLE_URL = "https://kachi-dev.github.io/uma-tools/umalator-global/bundle.js"
ANCHOR = '"200592":["Position Pilfer"]'  # known-good pair to locate the name map
OUT = Path(__file__).resolve().parent / "skills.json"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "uma-knowledge-tools skill-db"})
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


def extract_name_map(bundle):
    """Parse the {"<id>":["<global name>"], ...} JSON object around the anchor."""
    i = bundle.find(ANCHOR)
    if i < 0:
        sys.exit("error: anchor pair not found in bundle.js — bundle format changed?")
    start = bundle.rfind("{", 0, i)
    depth = 0
    for j in range(start, len(bundle)):
        if bundle[j] == "{":
            depth += 1
        elif bundle[j] == "}":
            depth -= 1
            if depth == 0:
                blob = bundle[start:j + 1]
                # minified JS uses \xHH escapes, which JSON doesn't allow
                blob = re.sub(r"\\x([0-9a-fA-F]{2})", r"\\u00\1", blob)
                return json.loads(blob)
    sys.exit("error: unbalanced braces extracting name map from bundle.js")


def main():
    meta = json.loads(fetch(META_URL))
    names = extract_name_map(fetch(BUNDLE_URL))
    print(f"fetched {len(meta)} meta entries, {len(names)} global names")

    skills = {}
    for sid, namelist in sorted(names.items()):
        name = namelist[0]
        m = meta.get(sid, {})
        gold = False
        pair_id = None
        middle_id = None
        if re.fullmatch(r"2\d{5}", sid):
            stem, suffix = sid[:-1], sid[-1]
            if suffix in "12":
                sibling = stem + ("2" if suffix == "1" else "1")
                if sibling in names:
                    gold = suffix == "1"
                    pair_id = sibling
            elif suffix == "4":
                # green-family rare gold: bundle chain is ○ (…2) -> ◎ (…1) -> gold
                if stem + "2" in names:
                    gold = True
                    pair_id = stem + "2"
                    middle_id = stem + "1" if stem + "1" in names else None
        entry = {
            "id": sid,
            "baseCost": m.get("baseCost"),
            "groupId": m.get("groupId"),
            "gold": gold,
            "pair": names[pair_id][0] if pair_id else None,
        }
        if middle_id:
            entry["middle"] = names[middle_id][0]
        # a unique (1xxxxx, baseCost 0) and its purchasable inherited version
        # (9xxxxx) share a name — keep the purchasable one
        if name not in skills or (not skills[name]["baseCost"] and m.get("baseCost")):
            skills[name] = entry

    OUT.write_text(json.dumps(
        {"fetched": date.today().isoformat(),
         "sources": [META_URL, BUNDLE_URL],
         "skills": skills},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    paired = sum(1 for s in skills.values() if s["pair"])
    print(f"wrote {OUT.name}: {len(skills)} skills, {paired} in gold/white pairs")


if __name__ == "__main__":
    main()
