#!/usr/bin/env python3
# SPDX-License-Identifier: CC-BY-SA-4.0
"""Flatten and optimise the logo SVGs.

Two passes:

1. **Flatten.**  A `.typ` source is exported to SVG by Typst, and both the art
   and every emoji glyph come back as a base64 `data:` URI inside `<image>`.
   That hides the drawing from diffs and grep, and makes a renderer rasterise
   a small bitmap and scale it up -- fuzzy edges at icon sizes.  Each `<image>`
   is therefore replaced by the SVG it points at: the inner `<svg>` takes the
   `<image>`'s rectangle and keeps its own viewBox and content attributes,
   wrapped in a `<g>` carrying the position/transform, with its ids namespaced
   so an inlined document cannot capture a reference from its host.

2. **Optimise.**  svgo, configured to keep the structure that carries the
   drawing: ids (they are what `use`/`clip-path` point at), groups (they carry
   the transforms) and clip paths.

Run `python3 scripts/build-svg.py` from the repository root, or name files.
"""

from __future__ import annotations

import base64
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_RE = re.compile(r"data:image/([\w+.-]+);base64,([A-Za-z0-9+/=\s]+)")
IMAGE_RE = re.compile(r"<image\b[^>]*?/>|<image\b[^>]*?>.*?</image>", re.S)
ATTR_RE = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')
ID_RE = re.compile(r'\bid="([^"]+)"')

# Attributes of the <image> that position it in the host document.  The rest of
# the <image> (opacity, style, clip-path, ...) transfers to the wrapper <g>.
WRAPPER_ATTRS = ("x", "y", "transform", "opacity", "style", "class",
                 "clip-path", "mask", "filter")
# Attributes the surface <svg> takes over from the <image>.
SURFACE_ATTRS = ("width", "height", "preserveAspectRatio")

SVGO_CONFIG = """\
// Keep the structure that carries the drawing: ids are what <use> and
// clip-path point at, and groups carry the transforms.
export default {
  multipass: true,
  floatPrecision: 4,
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          cleanupIds: false,
          collapseGroups: false,
          convertShapeToPath: false,
          mergePaths: false,
          removeHiddenElems: false,
          inlineStyles: false,
          minifyStyles: false,
        },
      },
    },
    { name: 'removeUnknownsAndDefaults', params: { keepRoleAttr: true } },
    'convertColors',
  ],
};
"""


def attrs(tag: str) -> dict[str, str]:
    return dict(ATTR_RE.findall(tag.split(">", 1)[0]))


def namespace_ids(body: str, prefix: str) -> str:
    ids = ID_RE.findall(body)
    for old in ids:
        new = prefix + old
        body = re.sub(r'\bid="%s"' % re.escape(old), 'id="%s"' % new, body)
        body = body.replace("url(#%s)" % old, "url(#%s)" % new)
        body = body.replace('href="#%s"' % old, 'href="#%s"' % new)
    return body


def inline_once(text: str, counter: list[int]) -> str:
    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        host = attrs(tag)
        href = host.get("xlink:href") or host.get("href") or ""
        m = DATA_RE.search(href)
        if not m or not m.group(1).endswith("svg+xml"):
            return tag
        inner = base64.b64decode(re.sub(r"\s+", "", m.group(2))).decode("utf-8")
        inner = re.sub(r"<\?xml[^>]*\?>", "", inner)
        inner = re.sub(r"<!DOCTYPE[^>]*>", "", inner)
        doc = re.search(r"<svg\b([^>]*)>(.*)</svg>", inner, re.S)
        if not doc:
            return tag
        counter[0] += 1
        body = namespace_ids(doc.group(2), "i%d_" % counter[0])

        surface = {k: v for k, v in attrs(doc.group(1)).items()
                   if k not in ("width", "height", "x", "y")}
        for name in SURFACE_ATTRS:
            if name in host and name not in surface:
                surface[name] = host[name]
        for name in ("width", "height"):
            if name in host:
                surface[name] = host[name]

        wrapper: dict[str, str] = {}
        for name in WRAPPER_ATTRS:
            if name in host:
                wrapper[name] = host[name]
        for name, value in host.items():
            if name in ("xlink:href", "href", "preserveAspectRatio",
                        "width", "height"):
                continue
            wrapper.setdefault(name, value)

        face = "".join(' %s="%s"' % kv for kv in surface.items())
        wrap = "".join(' %s="%s"' % kv for kv in wrapper.items())
        return "<g%s><svg%s>%s</svg></g>" % (wrap, face, body)

    return IMAGE_RE.sub(repl, text)


def flatten(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    before = len(text)
    counter = [0]
    for _ in range(8):  # nesting is shallow, but be safe
        new = inline_once(text, counter)
        if new == text:
            break
        text = new
    if "data:image" in text:
        raise SystemExit("%s still carries a data: URI" % path)
    path.write_text(text, encoding="utf-8")
    print("%-30s flatten %6d -> %6d" % (path.relative_to(ROOT), before, len(text)))
    return True


def optimise(paths: list[Path]) -> None:
    svgo = shutil.which("svgo")
    if svgo is None:
        raise SystemExit("svgo not found; install it (npm i -g svgo)")
    config = ROOT / "scripts" / "svgo.config.mjs"
    config.write_text(SVGO_CONFIG, encoding="utf-8")
    for path in paths:
        before = path.stat().st_size
        subprocess.run(
            [svgo, "--config", str(config), "-i", str(path), "-o", str(path)],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        print("%-30s svgo    %6d -> %6d" % (path.relative_to(ROOT), before,
                                            path.stat().st_size))


def main(argv: list[str]) -> int:
    targets = [Path(a) for a in argv] or sorted(ROOT.glob("*.svg"))
    targets = [p if p.is_absolute() else ROOT / p for p in targets]
    for path in targets:
        flatten(path)
    optimise(targets)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
