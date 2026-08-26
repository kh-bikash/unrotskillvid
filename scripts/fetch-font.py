#!/usr/bin/env python3
"""Download a Google font's latin-subset woff2 files and print the @font-face block.

    python scripts/fetch-font.py "Geist" 400 500 600 700 --dir assets/fonts
"""

import argparse
import pathlib
import re
import sys
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req) as r:
        return r.read()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("family", help='e.g. "Geist", "Inter", or "Plus Jakarta Sans"')
    ap.add_argument("weights", nargs="+", help="e.g. 400 600 700")
    ap.add_argument("--dir", required=True, help="output directory, e.g. assets/fonts")
    ap.add_argument("--css-path", default="assets/fonts",
                    help="path prefix used inside the composition CSS (default assets/fonts)")
    args = ap.parse_args()

    slug = re.sub(r"[^a-z0-9]+", "-", args.family.lower()).strip("-")
    spec = ";".join(sorted(set(args.weights), key=int))
    url = (f"https://fonts.googleapis.com/css2?family="
           f"{urllib.parse.quote(args.family)}:wght@{spec}&display=swap")

    try:
        css = fetch(url).decode("utf-8")
    except Exception as exc:
        sys.exit(f"Could not fetch CSS for {args.family!r}: {exc}\n"
                 f"Check the family name and weights exist on Google Fonts.")

    out = pathlib.Path(args.dir)
    out.mkdir(parents=True, exist_ok=True)

    got = {}
    for block in re.findall(r"@font-face\s*\{(.*?)\}", css, re.S):
        w = re.search(r"font-weight:\s*(\d+)", block)
        u = re.search(r"url\((https://[^)]+\.woff2)\)", block)
        ur = re.search(r"unicode-range:\s*([^;]+);", block)
        if not (w and u and ur):
            continue
        if "U+0000-00FF" not in ur.group(1):     # latin subset only
            continue
        weight = w.group(1)
        if weight in got:
            continue
        dest = out / f"{slug}-{weight}.woff2"
        dest.write_bytes(fetch(u.group(1)))
        got[weight] = dest

    missing = sorted(set(args.weights) - set(got), key=int)
    if missing:
        print(f"WARNING: no latin face returned for weight(s) {', '.join(missing)} — "
              f"the family may not ship them.", file=sys.stderr)
    if not got:
        sys.exit("Nothing downloaded.")

    total = sum(p.stat().st_size for p in got.values())
    print(f"\nDownloaded {len(got)} face(s) to {out}  ({total // 1024} KB)\n")
    print("Paste into each composition's <style>:\n")
    for weight in sorted(got, key=int):
        print(f'      @font-face {{ font-family: "{args.family}"; font-style: normal; '
              f'font-weight: {weight}; font-display: block; '
              f'src: url({args.css_path}/{slug}-{weight}.woff2) format("woff2"); }}')
    print(f'\n      /* then: font-family: "{args.family}", sans-serif; */\n')


if __name__ == "__main__":
    main()
