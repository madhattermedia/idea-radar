#!/usr/bin/env python3
"""Idea radar spreadsheet helper. Standard library only.

  sheet.py list <ideas.csv>              what is already on the sheet (JSON)
  sheet.py add  <ideas.csv> <new.json>   validate and append new ideas

The sheet is a CSV with a byte order mark so Excel reads the encoding correctly.
Existing rows are never rewritten: Status and Notes belong to the person using it.
"""
import csv
import datetime
import json
import os
import re
import sys

COLUMNS = [
    ("id", "ID"),
    ("found", "Date found"),
    ("pillar", "Pillar"),
    ("story", "Story"),
    ("source", "Source"),
    ("url", "Link"),
    ("published", "Published"),
    ("what_happened", "What happened"),
    ("angle", "Angle"),
    ("belief", "Belief it comes from"),
    ("hook", "Hook"),
    ("alt_hook", "Alternate hook"),
    ("text_hook", "Text on screen"),
    ("format", "Format"),
    ("platform", "Platform"),
    ("why_now", "Why now"),
    ("heat", "Heat (1-3)"),
    ("status", "Status"),
    ("notes", "Notes"),
]
HEADERS = [label for _, label in COLUMNS]
REQUIRED = ["pillar", "story", "source", "url", "what_happened", "angle", "belief",
            "hook", "alt_hook", "text_hook", "format", "platform", "why_now"]
WRITTEN_BY_US = ["what_happened", "angle", "belief", "hook", "alt_hook", "text_hook",
                 "format", "why_now"]
TRACKING = re.compile(r"^(utm_|fbclid|gclid|mc_|ref$)", re.I)


def norm_url(url):
    """Same article, same key: ignore scheme, www, tracking parameters, trailing slash."""
    url = (url or "").strip()
    url = re.sub(r"#.*$", "", url)
    base, _, query = url.partition("?")
    kept = [p for p in query.split("&") if p and not TRACKING.match(p)]
    base = re.sub(r"^https?://(www\.)?", "", base, flags=re.I).rstrip("/").lower()
    return base + ("?" + "&".join(kept) if kept else "")


def read_rows(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def cmd_list(path):
    rows = read_rows(path)
    out = [{"id": r.get("ID", ""), "found": r.get("Date found", ""),
            "pillar": r.get("Pillar", ""), "story": r.get("Story", ""), "source": r.get("Source", ""),
            "url": r.get("Link", ""), "hook": r.get("Hook", "")} for r in rows]
    print(json.dumps({"sheet": path, "count": len(out), "ideas": out}, indent=1,
                     ensure_ascii=False))


def check(idea, n):
    problems = []
    for key in REQUIRED:
        if not str(idea.get(key, "")).strip():
            problems.append(f"idea {n}: '{key}' is empty")
    url = str(idea.get("url", "")).strip()
    if url and not re.match(r"^https?://\S+\.\S+", url):
        problems.append(f"idea {n}: link is not a web address: {url}")
    for key in WRITTEN_BY_US:
        text = str(idea.get(key, ""))
        if "—" in text or "–" in text:
            problems.append(f"idea {n}: '{key}' contains an em or en dash")
        if "!" in text:
            problems.append(f"idea {n}: '{key}' contains an exclamation mark")
    try:
        if int(idea.get("heat", 2)) not in (1, 2, 3):
            raise ValueError
    except (TypeError, ValueError):
        problems.append(f"idea {n}: heat must be 1, 2 or 3")
    published = str(idea.get("published", "")).strip()
    if published and not re.match(r"^\d{4}-\d{2}-\d{2}$", published):
        problems.append(f"idea {n}: published must be YYYY-MM-DD or empty")
    return problems


def cmd_add(path, json_path):
    with open(json_path, encoding="utf-8") as f:
        ideas = json.load(f)
    if not isinstance(ideas, list):
        sys.exit("The JSON file must be a list of ideas.")

    problems = []
    for n, idea in enumerate(ideas, 1):
        if not isinstance(idea, dict):
            problems.append(f"idea {n}: not an object")
        else:
            problems += check(idea, n)
    if problems:
        print("Nothing was added. Fix these and run again:")
        for p in problems:
            print("  - " + p)
        sys.exit(1)

    existing = read_rows(path)
    if existing and list(existing[0].keys()) != HEADERS:
        sys.exit("The sheet's columns have been changed, so rows can't be added "
                 "safely. Restore the original header row and run again.")
    seen = {norm_url(r.get("Link", "")) for r in existing}
    today = datetime.date.today()
    prefix = today.strftime("%Y%m%d")
    taken = [int(r["ID"].split("-")[1]) for r in existing
             if re.match(rf"^{prefix}-\d+$", r.get("ID", ""))]
    counter = max(taken, default=0)

    added, skipped = [], []
    for idea in ideas:
        key = norm_url(idea["url"])
        if key in seen:
            skipped.append(idea["story"])
            continue
        seen.add(key)
        counter += 1
        row = {k: " ".join(str(idea.get(k, "")).split()) for k, _ in COLUMNS}
        row.update(id=f"{prefix}-{counter:02d}", found=today.isoformat(),
                   heat=int(idea.get("heat", 2)), status="New", notes="")
        added.append(row)

    if added:
        folder = os.path.dirname(os.path.abspath(path))
        os.makedirs(folder, exist_ok=True)
        new_file = not os.path.exists(path)
        with open(path, "a", newline="", encoding="utf-8-sig" if new_file else "utf-8") as f:
            writer = csv.writer(f)
            if new_file:
                writer.writerow(HEADERS)
            for row in added:
                writer.writerow([row[k] for k, _ in COLUMNS])

    print(f"Added {len(added)} idea(s) to {path}.")
    for row in added:
        print(f"  {row['id']}  {row['hook']}")
    if skipped:
        print(f"Skipped {len(skipped)} already on the sheet:")
        for story in skipped:
            print(f"  - {story}")


def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == "list":
        cmd_list(os.path.expanduser(args[1]))
    elif len(args) == 3 and args[0] == "add":
        cmd_add(os.path.expanduser(args[1]), os.path.expanduser(args[2]))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
