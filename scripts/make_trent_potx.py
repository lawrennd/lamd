#!/usr/bin/env python3
"""
Generate trent-reference.potx — a Trent.AI-branded PowerPoint template
for use with pandoc's --reference-doc flag.

Usage:
    python3 scripts/make_trent_potx.py

Outputs:
    lamd/includes/trent-reference.potx

Requires: python-pptx
    pip install python-pptx --break-system-packages
"""

import copy
import os
import shutil
import zipfile
from pathlib import Path
from lxml import etree

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT   = SCRIPT_DIR.parent          # lamd/
SOURCE_POTX = REPO_ROOT / "lamd" / "includes" / "custom-reference.potx"
OUTPUT_POTX = REPO_ROOT / "lamd" / "includes" / "trent-reference.potx"

# Trent assets (from the slides repo sibling to talks)
SLIDES_ROOT  = REPO_ROOT.parent.parent / "lawrennd" / "slides"
PHOTO_PATH   = SLIDES_ROOT / "diagrams" / "people" / "neil-trent-portrait.jpg"
LOGO_PATH    = SLIDES_ROOT / "diagrams" / "logos" / "trent-blue.png"

WORK_DIR = Path("/tmp/trent_potx_work")

# ---------------------------------------------------------------------------
# Trent palette (hex without #)
# ---------------------------------------------------------------------------
ORANGE  = "F5821F"   # primary accent — headings, highlights
NAVY    = "1A1A3E"   # dark text
PEACH   = "FDE9D8"   # light background / gradient start
PEACH2  = "FAE0C8"   # gradient end
WHITE   = "FFFFFF"
GREY    = "6A6A8A"   # muted text

# EMU constants (914400 EMU = 1 inch)
EMU = 914400
# Standard widescreen slide: 10 × 7.5 inches → check source first, fallback here
SLIDE_W = 9144000   # 10 inches — may be overridden after reading source
SLIDE_H = 6858000   # 7.5 inches

NS = {
    "a":  "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p":  "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r":  "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel":"http://schemas.openxmlformats.org/package/2006/relationships",
}
for prefix, uri in NS.items():
    etree.register_namespace(prefix, uri)


def a(tag):
    return "{%s}%s" % (NS["a"], tag)

def p(tag):
    return "{%s}%s" % (NS["p"], tag)

def r_ns(tag):
    return "{%s}%s" % (NS["r"], tag)


# ---------------------------------------------------------------------------
# Step 1 — Unpack source POTX
# ---------------------------------------------------------------------------
def unpack(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    with zipfile.ZipFile(src) as z:
        z.extractall(dst)


# ---------------------------------------------------------------------------
# Step 2 — Patch theme XML
# ---------------------------------------------------------------------------
def patch_theme(work: Path):
    theme_path = work / "ppt" / "theme" / "theme1.xml"
    tree = etree.parse(str(theme_path))
    root = tree.getroot()

    # Colour scheme
    clr_scheme = root.find(f".//{a('clrScheme')}")
    if clr_scheme is not None:
        # Map: dk1=black, lt1=white, dk2=navy, lt2=peach, accent1=orange
        mapping = {
            "dk1":     ("sysClr", {"val": "windowText", "lastClr": "000000"}),
            "lt1":     ("sysClr", {"val": "window",     "lastClr": "FFFFFF"}),
            "dk2":     ("srgbClr", {"val": NAVY}),
            "lt2":     ("srgbClr", {"val": PEACH}),
            "accent1": ("srgbClr", {"val": ORANGE}),
            "accent2": ("srgbClr", {"val": PEACH2}),
            "accent3": ("srgbClr", {"val": "D4EDDA"}),   # soft green tint
            "accent4": ("srgbClr", {"val": "B8D4F5"}),   # soft blue tint
            "accent5": ("srgbClr", {"val": "F5C6A0"}),   # warm peach mid
            "accent6": ("srgbClr", {"val": "C8650F"}),   # darker orange
            "hlink":   ("srgbClr", {"val": ORANGE}),
            "folHlink":("srgbClr", {"val": "C8650F"}),
        }
        for slot_tag, (clr_tag, attrs) in mapping.items():
            slot = clr_scheme.find(a(slot_tag))
            if slot is None:
                slot = etree.SubElement(clr_scheme, a(slot_tag))
            # Remove existing children
            for child in list(slot):
                slot.remove(child)
            child = etree.SubElement(slot, a(clr_tag))
            for k, v in attrs.items():
                child.set(k, v)

    # Font scheme — switch to Inter
    font_scheme = root.find(f".//{a('fontScheme')}")
    if font_scheme is not None:
        for major_minor in [a("majorFont"), a("minorFont")]:
            node = font_scheme.find(major_minor)
            if node is not None:
                latin = node.find(a("latin"))
                if latin is None:
                    latin = etree.SubElement(node, a("latin"))
                latin.set("typeface", "Inter")

    tree.write(str(theme_path), xml_declaration=True,
               encoding="UTF-8", standalone=True)
    print("  ✓ theme patched")


# ---------------------------------------------------------------------------
# Step 3 — Patch Title Slide layout (slideLayout1.xml)
#           — peach gradient left panel, white right panel, photo + logo
# ---------------------------------------------------------------------------
def patch_title_layout(work: Path):
    layout_path = work / "ppt" / "slideLayouts" / "slideLayout1.xml"
    tree = etree.parse(str(layout_path))
    root = tree.getroot()

    # Read actual slide dimensions from presentation.xml
    prs_path = work / "ppt" / "presentation.xml"
    prs_tree = etree.parse(str(prs_path))
    sldSz = prs_tree.getroot().find(p("sldSz"))
    w = int(sldSz.get("cx", SLIDE_W)) if sldSz is not None else SLIDE_W
    h = int(sldSz.get("cy", SLIDE_H)) if sldSz is not None else SLIDE_H

    split = int(w * 0.57)   # left panel width (57%)
    right_x = split
    right_w = w - split

    # ---- Background: left peach, right white (two-rect approach) -----------
    # We set the slide background to white, then add two rectangles
    # to the spTree before the placeholders.

    cSld = root.find(p("cSld"))

    # Set slide background to white
    bg = cSld.find(p("bg"))
    if bg is None:
        bg = etree.SubElement(cSld, p("bg"))
    bgPr = bg.find(p("bgPr"))
    if bgPr is None:
        bgPr = etree.SubElement(bg, p("bgPr"))
    for child in list(bgPr):
        bgPr.remove(child)
    solidFill = etree.SubElement(bgPr, a("solidFill"))
    srgbClr = etree.SubElement(solidFill, a("srgbClr"))
    srgbClr.set("val", WHITE)

    spTree = cSld.find(p("spTree"))

    def make_rect(sp_id, name, x, y, cx, cy, fill_xml, z_order=None):
        """Return a <p:sp> rectangle element."""
        sp = etree.Element(p("sp"))
        nvSpPr = etree.SubElement(sp, p("nvSpPr"))
        cNvPr  = etree.SubElement(nvSpPr, p("cNvPr"))
        cNvPr.set("id", str(sp_id))
        cNvPr.set("name", name)
        cNvSpPr = etree.SubElement(nvSpPr, p("cNvSpPr"))
        nvPr    = etree.SubElement(nvSpPr, p("nvPr"))

        spPr = etree.SubElement(sp, p("spPr"))
        xfrm = etree.SubElement(spPr, a("xfrm"))
        off  = etree.SubElement(xfrm, a("off"))
        off.set("x", str(x)); off.set("y", str(y))
        ext  = etree.SubElement(xfrm, a("ext"))
        ext.set("cx", str(cx)); ext.set("cy", str(cy))
        prstGeom = etree.SubElement(spPr, a("prstGeom"))
        prstGeom.set("prst", "rect")
        etree.SubElement(prstGeom, a("avLst"))
        spPr.append(etree.fromstring(fill_xml))
        ln = etree.SubElement(spPr, a("ln"))
        etree.SubElement(ln, a("noFill"))

        txBody = etree.SubElement(sp, p("txBody"))
        etree.SubElement(txBody, a("bodyPr"))
        etree.SubElement(txBody, a("lstStyle"))
        etree.SubElement(txBody, a("p"))
        return sp

    # Left panel: gradient peach fill
    LEFT_FILL = f"""<a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" rotWithShape="1">
      <a:gsLst>
        <a:gs pos="0">
          <a:srgbClr val="{PEACH}"/>
        </a:gs>
        <a:gs pos="100000">
          <a:srgbClr val="{PEACH2}"/>
        </a:gs>
      </a:gsLst>
      <a:lin ang="10800000" scaled="0"/>
    </a:gradFill>"""

    # Right panel: white
    RIGHT_FILL = f"""<a:solidFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
      <a:srgbClr val="{WHITE}"/>
    </a:solidFill>"""

    left_rect  = make_rect(100, "LeftPanel",  0,       0, split,   h, LEFT_FILL)
    right_rect = make_rect(101, "RightPanel", right_x, 0, right_w, h, RIGHT_FILL)

    # Insert background rects at position 1 (after nvGrpSpPr/grpSpPr)
    # Find grpSpPr to insert after it
    grpSpPr_idx = None
    for i, child in enumerate(spTree):
        if child.tag == p("grpSpPr"):
            grpSpPr_idx = i
            break
    insert_at = (grpSpPr_idx + 1) if grpSpPr_idx is not None else 0
    spTree.insert(insert_at, right_rect)
    spTree.insert(insert_at, left_rect)

    # ---- Reposition existing title placeholder into left panel -------------
    for sp in spTree.findall(p("sp")):
        nvSpPr = sp.find(p("nvSpPr"))
        if nvSpPr is None:
            continue
        nvPr = nvSpPr.find(p("nvPr"))
        if nvPr is None:
            continue
        ph = nvPr.find(p("ph"))
        if ph is None:
            continue
        ph_type = ph.get("type", "")

        spPr = sp.find(p("spPr"))
        if spPr is None:
            spPr = etree.SubElement(sp, p("spPr"))

        xfrm = spPr.find(a("xfrm"))
        if xfrm is None:
            xfrm = etree.SubElement(spPr, a("xfrm"))

        def set_xfrm(xf, x, y, cx, cy):
            off = xf.find(a("off"))
            if off is None: off = etree.SubElement(xf, a("off"))
            off.set("x", str(x)); off.set("y", str(y))
            ext = xf.find(a("ext"))
            if ext is None: ext = etree.SubElement(xf, a("ext"))
            ext.set("cx", str(cx)); ext.set("cy", str(cy))

        margin = int(0.35 * EMU)   # ~0.35 inch margin
        top_logo = int(0.65 * EMU) # space for logo at top

        if ph_type in ("ctrTitle", "title"):
            # Title: large, left-panel, orange
            set_xfrm(xfrm,
                     margin,
                     int(h * 0.22),
                     split - 2 * margin,
                     int(h * 0.52))
            # Force title colour to orange
            txBody = sp.find(p("txBody"))
            if txBody is not None:
                lstStyle = txBody.find(a("lstStyle"))
                if lstStyle is None:
                    lstStyle = etree.SubElement(txBody, a("lstStyle"))
                lvl1 = lstStyle.find(a("lvl1pPr"))
                if lvl1 is None:
                    lvl1 = etree.SubElement(lstStyle, a("lvl1pPr"))
                lvl1.set("algn", "l")
                defRPr = lvl1.find(a("defRPr"))
                if defRPr is None:
                    defRPr = etree.SubElement(lvl1, a("defRPr"))
                defRPr.set("sz", "3600")
                defRPr.set("b", "1")
                # Remove existing effects / colour
                for child in list(defRPr):
                    defRPr.remove(child)
                solidFill = etree.SubElement(defRPr, a("solidFill"))
                srgb = etree.SubElement(solidFill, a("srgbClr"))
                srgb.set("val", ORANGE)

        elif ph_type == "subTitle":
            # Subtitle: below title, left panel
            set_xfrm(xfrm,
                     margin,
                     int(h * 0.76),
                     split - 2 * margin,
                     int(h * 0.20))
            txBody = sp.find(p("txBody"))
            if txBody is not None:
                lstStyle = txBody.find(a("lstStyle"))
                if lstStyle is None:
                    lstStyle = etree.SubElement(txBody, a("lstStyle"))
                lvl1 = lstStyle.find(a("lvl1pPr"))
                if lvl1 is None:
                    lvl1 = etree.SubElement(lstStyle, a("lvl1pPr"))
                lvl1.set("algn", "l")
                defRPr = lvl1.find(a("defRPr"))
                if defRPr is None:
                    defRPr = etree.SubElement(lvl1, a("defRPr"))
                defRPr.set("sz", "1800")
                defRPr.set("b", "0")
                for child in list(defRPr):
                    defRPr.remove(child)
                solidFill = etree.SubElement(defRPr, a("solidFill"))
                srgb = etree.SubElement(solidFill, a("srgbClr"))
                srgb.set("val", NAVY)

    # ---- Photo placeholder in right panel ----------------------------------
    photo_margin = int(0.3 * EMU)
    photo_x  = right_x + photo_margin
    photo_y  = int(h * 0.08)
    photo_cx = right_w - 2 * photo_margin
    photo_cy = int(h * 0.70)

    # Add picture placeholder (type="pic") for the speaker photo
    pic_sp = etree.SubElement(spTree, p("sp"))
    pic_nvSpPr  = etree.SubElement(pic_sp, p("nvSpPr"))
    pic_cNvPr   = etree.SubElement(pic_nvSpPr, p("cNvPr"))
    pic_cNvPr.set("id", "102"); pic_cNvPr.set("name", "SpeakerPhoto")
    pic_cNvSpPr = etree.SubElement(pic_nvSpPr, p("cNvSpPr"))
    pic_nvPr    = etree.SubElement(pic_nvSpPr, p("nvPr"))
    pic_ph      = etree.SubElement(pic_nvPr, p("ph"))
    pic_ph.set("type", "pic")
    pic_ph.set("idx", "1")

    pic_spPr = etree.SubElement(pic_sp, p("spPr"))
    pic_xfrm = etree.SubElement(pic_spPr, a("xfrm"))
    pic_off  = etree.SubElement(pic_xfrm, a("off"))
    pic_off.set("x", str(photo_x)); pic_off.set("y", str(photo_y))
    pic_ext  = etree.SubElement(pic_xfrm, a("ext"))
    pic_ext.set("cx", str(photo_cx)); pic_ext.set("cy", str(photo_cy))
    pic_geom = etree.SubElement(pic_spPr, a("prstGeom"))
    pic_geom.set("prst", "roundRect")
    pic_avLst= etree.SubElement(pic_geom, a("avLst"))
    pic_gd   = etree.SubElement(pic_avLst, a("gd"))
    pic_gd.set("name", "adj"); pic_gd.set("fmla", "val 16667")  # ~corner radius
    etree.SubElement(pic_spPr, a("noFill"))

    pic_txBody = etree.SubElement(pic_sp, p("txBody"))
    etree.SubElement(pic_txBody, a("bodyPr"))
    etree.SubElement(pic_txBody, a("lstStyle"))
    p_el = etree.SubElement(pic_txBody, a("p"))
    r_el = etree.SubElement(p_el, a("r"))
    etree.SubElement(r_el, a("rPr")).set("lang", "en-GB")
    etree.SubElement(r_el, a("t"))

    # ---- Speaker name text box (below photo) --------------------------------
    name_x  = right_x + photo_margin
    name_y  = photo_y + photo_cy + int(0.12 * EMU)
    name_cx = right_w - 2 * photo_margin
    name_cy = int(0.35 * EMU)

    name_sp = make_rect(103, "SpeakerName", name_x, name_y, name_cx, name_cy,
                        f'<a:noFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
    # Override txBody with styled text placeholder
    name_txBody = name_sp.find(p("txBody"))
    for child in list(name_txBody):
        name_txBody.remove(child)
    name_bodyPr = etree.SubElement(name_txBody, a("bodyPr"))
    name_bodyPr.set("anchor", "ctr")
    etree.SubElement(name_txBody, a("lstStyle"))
    name_p = etree.SubElement(name_txBody, a("p"))
    name_pPr = etree.SubElement(name_p, a("pPr"))
    name_pPr.set("algn", "ctr")
    name_r = etree.SubElement(name_p, a("r"))
    name_rPr = etree.SubElement(name_r, a("rPr"))
    name_rPr.set("lang", "en-GB"); name_rPr.set("sz", "1400"); name_rPr.set("b", "1")
    name_solidFill = etree.SubElement(name_rPr, a("solidFill"))
    name_srgb = etree.SubElement(name_solidFill, a("srgbClr"))
    name_srgb.set("val", NAVY)
    name_t = etree.SubElement(name_r, a("t"))
    name_t.text = "Neil D. Lawrence"
    spTree.append(name_sp)

    # ---- Role / institute text box ------------------------------------------
    role_y  = name_y + name_cy + int(0.05 * EMU)
    role_cy = int(0.40 * EMU)
    role_sp = make_rect(104, "SpeakerRole", name_x, role_y, name_cx, role_cy,
                        f'<a:noFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
    role_txBody = role_sp.find(p("txBody"))
    for child in list(role_txBody):
        role_txBody.remove(child)
    role_bodyPr = etree.SubElement(role_txBody, a("bodyPr"))
    role_bodyPr.set("anchor", "ctr")
    etree.SubElement(role_txBody, a("lstStyle"))
    role_p = etree.SubElement(role_txBody, a("p"))
    role_pPr = etree.SubElement(role_p, a("pPr"))
    role_pPr.set("algn", "ctr")
    role_r = etree.SubElement(role_p, a("r"))
    role_rPr = etree.SubElement(role_r, a("rPr"))
    role_rPr.set("lang", "en-GB"); role_rPr.set("sz", "1100")
    role_solidFill = etree.SubElement(role_rPr, a("solidFill"))
    role_srgb = etree.SubElement(role_solidFill, a("srgbClr"))
    role_srgb.set("val", GREY)
    role_t = etree.SubElement(role_r, a("t"))
    role_t.text = "Chief Scientist & Co-Founder, Trent AI"
    spTree.append(role_sp)

    tree.write(str(layout_path), xml_declaration=True,
               encoding="UTF-8", standalone=True)
    print("  ✓ title slide layout patched")


# ---------------------------------------------------------------------------
# Step 4 — Patch content slide master heading colour
# ---------------------------------------------------------------------------
def patch_master(work: Path):
    master_dir = work / "ppt" / "slideMasters"
    for master_file in master_dir.glob("slideMaster*.xml"):
        tree = etree.parse(str(master_file))
        root = tree.getroot()
        # Find txStyles → title style → set colour to ORANGE
        txStyles = root.find(p("txStyles"))
        if txStyles is not None:
            titleStyle = txStyles.find(p("titleStyle"))
            if titleStyle is not None:
                lvl1 = titleStyle.find(a("lvl1pPr"))
                if lvl1 is None:
                    lvl1 = etree.SubElement(titleStyle, a("lvl1pPr"))
                defRPr = lvl1.find(a("defRPr"))
                if defRPr is None:
                    defRPr = etree.SubElement(lvl1, a("defRPr"))
                for child in list(defRPr):
                    defRPr.remove(child)
                solidFill = etree.SubElement(defRPr, a("solidFill"))
                srgb = etree.SubElement(solidFill, a("srgbClr"))
                srgb.set("val", ORANGE)
        tree.write(str(master_file), xml_declaration=True,
                   encoding="UTF-8", standalone=True)
    print("  ✓ slide master heading colour patched")


# ---------------------------------------------------------------------------
# Step 5 — Repack as POTX
# ---------------------------------------------------------------------------
def repack(work: Path, output: Path):
    output.unlink(missing_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        for fpath in sorted(work.rglob("*")):
            if fpath.is_file():
                zf.write(fpath, fpath.relative_to(work))
    print(f"  ✓ packed → {output}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Building trent-reference.potx …")

    if not SOURCE_POTX.exists():
        print(f"ERROR: source POTX not found at {SOURCE_POTX}")
        return 1

    print(f"  source : {SOURCE_POTX}")

    # Unpack
    unpack(SOURCE_POTX, WORK_DIR)

    # Patch
    patch_theme(WORK_DIR)
    patch_title_layout(WORK_DIR)
    patch_master(WORK_DIR)

    # Repack
    repack(WORK_DIR, OUTPUT_POTX)

    print(f"\nDone. To use, add to your talk frontmatter:")
    print(f"  pptx: True")
    print(f"  potx: {OUTPUT_POTX}")
    print()
    print("Note: the speaker photo placeholder on the cover slide")
    print("needs to be filled in PowerPoint (right-click → Change Picture).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
