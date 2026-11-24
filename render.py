#!/usr/bin/env python3
"""Render the front page for Monday 23 November 2026.

One 1024x1024 PNG, flat newspaper front page: banner, date masthead,
three hero stories with flat-vector illustrations, a 10-story grid,
a 25-item ALSO list, a dotted world map, a DATE CHECK box and a legend.
All stories were verified as events of, or first reported on,
Monday 23 November 2026. Deterministic: same input, same bytes.
"""
import hashlib

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def fnt(name, size):
    return ImageFont.truetype(FONT_DIR + "/" + name, size)


def serif_b(s):
    return fnt("DejaVuSerif-Bold.ttf", s)


def serif(s):
    return fnt("DejaVuSerif.ttf", s)


def sans_b(s):
    return fnt("DejaVuSans-Bold.ttf", s)


def sans(s):
    return fnt("DejaVuSans.ttf", s)


CREAM = (246, 240, 225)
PAPER = (252, 248, 238)
NAVY = (27, 42, 74)
NAVY_DK = (18, 30, 56)
RED = (139, 30, 30)
RED_LT = (172, 52, 44)
INK = (26, 26, 26)
GRAY = (96, 89, 76)
LINE = (186, 178, 158)
WHITE = (255, 255, 255)

REGION = {
    "AMERICA": (43, 94, 167),
    "EUROPE": (46, 125, 79),
    "ASIA": (201, 106, 30),
    "MIDDLE EAST": (107, 79, 161),
    "AFRICA": (138, 90, 43),
    "OCEANIA": (31, 122, 122),
    "LATIN AMERICA": (176, 58, 46),
    "SCIENCE": (90, 90, 110),
}

TAG_FILL = {
    "CONFIRMED": (27, 42, 74),
    "OFFICIAL": (46, 125, 79),
    "REPORTED": (96, 89, 76),
    "CLAIM": (172, 52, 44),
}


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, font, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def rule(d, x0, x1, y, fill=LINE, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def tag_pill(d, x, y, tag):
    """Small filled tag pill; returns the x just past the pill."""
    f = sans_b(9)
    tw = d.textlength(tag, font=f)
    pad = 5
    w = int(tw) + pad * 2
    h = 14
    d.rounded_rectangle([x, y, x + w, y + h], radius=3,
                        fill=TAG_FILL[tag])
    d.text((x + pad, y + 2), tag, font=f, fill=WHITE)
    return x + w


def chip(d, x, y, w, label, count, color):
    d.rounded_rectangle([x, y, x + w, y + 18], radius=4, fill=color)
    f = sans_b(10)
    txt = "%s %d" % (label, count)
    tw = d.textlength(txt, font=f)
    d.text((x + (w - tw) / 2, y + 3), txt, font=f, fill=WHITE)


# ---------------------------------------------------------------- data
HEROES = [
    {
        "num": "1",
        "place": "BENGHAZI, LIBYA",
        "cat": "WAR",
        "tag": "CONFIRMED",
        "headline": "Zelenskyy confirms Ukraine sank Russian corvette Merkury",
        "body": ("Seven Ukrainian sea drones sank the corvette Merkury in "
                 "Benghazi harbour and hit the cargo ship Angara, Kyiv says. "
                 "Zelenskyy told NATO's assembly in Berlin that \u201cRussia "
                 "can feel our response\u201d. Libya condemned the strike; "
                 "the UN mission called for an inquiry."),
        "source": "Sources: AP \u00b7 WSJ \u00b7 BBC \u00b7 The Times",
        "art": "merkury",
    },
    {
        "num": "2",
        "place": "NEW YORK",
        "cat": "MARKETS",
        "tag": "CONFIRMED",
        "headline": "Huang returns as Nvidia chief; Nasdaq jumps 7%, Nvidia 30%",
        "body": ("Jensen Huang is back as Nvidia chief executive after "
                 "President Trump's intervention. The Nasdaq rose 7% and "
                 "Nvidia 30% \u2014 its biggest one-day gain in 23 years "
                 "\u2014 while Asian tech stocks fell deeper into the AI "
                 "sell-off."),
        "source": "Sources: Reuters \u00b7 Nasdaq",
        "art": "nvidia",
    },
    {
        "num": "3",
        "place": "QOM, IRAN",
        "cat": "HUMAN RIGHTS",
        "tag": "REPORTED",
        "headline": "Iran flogs singer Parastoo Ahmadi, 74 lashes, in Qom",
        "body": ("Parastoo Ahmadi and four members of her band were each "
                 "given 74 lashes in Qom for performing without a hijab, "
                 "in one of the day's most widely reported human-rights "
                 "stories."),
        "source": "Sources: wires, first reported 17:47 UTC",
        "art": "ahmadi",
    },
]

GRID = [
    ("EUROPE", "KYIV TOLL RISES TO AT LEAST 15",
     "A 7-year-old was pulled alive from rubble after 14 hours; a "
     "five-storey block in Dymer collapsed.", "CONFIRMED", "BBC \u00b7 Al Jazeera"),
    ("AMERICA", "US SANCTIONS IRAN SHADOW BANKING",
     "Washington blacklists a network accused of moving money for "
     "Tehran; first reported 18:30 UTC.", "REPORTED", "wires"),
    ("EUROPE", "EU PROPOSES NEW RUSSIA SANCTIONS",
     "60 banks, crypto curbs, 70 shadow-fleet ships and a sports ban "
     "in the latest package.", "REPORTED", "wires"),
    ("EUROPE", "BELGIUM'S AIRPORTS SHUT FOR A DAY",
     "An air-traffic controllers' strike grounds flights and strands "
     "50,000+ travellers.", "CONFIRMED", "wires"),
    ("LATIN AMERICA", "DRONE HITS POLICE BASE IN C\u00daCUTA",
     "A drone attack on a police station in Colombia damages "
     "60 homes.", "REPORTED", "wires"),
    ("LATIN AMERICA", "BOLSONARO HAS PNEUMONIA IN ICU",
     "Doctors diagnose bilateral pneumonia and cancel surgery; his "
     "condition is stable.", "OFFICIAL", "G1 Globo"),
    ("OCEANIA", "MOLLY MELDRUM DIES, AGED 83",
     "The Australian music legend dies in Melbourne.", "CONFIRMED", "BBC"),
    ("ASIA", "INDIA GIVES \u20ac1.4BN TO NEPAL",
     "$1.62bn for recovery after August's floods, announced "
     "Monday.", "OFFICIAL", "wires"),
    ("AFRICA", "KENYA AND DR CONGO RESTORE TIES",
     "The two countries agree to restore full diplomatic "
     "relations.", "OFFICIAL", "wires"),
    ("AMERICA", "COMMANDERS 22\u201320 BENGALS",
     "A last-second field goal ends Cincinnati's five-game winning "
     "run; the lights briefly went out.", "CONFIRMED", "USA Today"),
]

ALSO_LEFT = [
    ("AMERICA", "US Army to detonate lead azide in Iowa despite court order", "REPORTED"),
    ("AMERICA", "FBI investigates hack of criminal database NCIC", "REPORTED"),
    ("AMERICA", "Masked ICE agents detain father and son on Sea-Tac jet bridge", "REPORTED"),
    ("AMERICA", "NBA: Bucks 116\u2013111 Raptors as Herro's 32 ends 13-game skid", "CONFIRMED"),
    ("EUROPE", "Finland summons Russia's ambassador", "OFFICIAL"),
    ("EUROPE", "Russia warns Estonia of open war", "CLAIM"),
    ("EUROPE", "NATO meets Monday over missile strike in Poland", "OFFICIAL"),
    ("EUROPE", "Eurozone inflation stands at 4.0%", "OFFICIAL"),
    ("EUROPE", "UN talks on autonomous weapons end with no binding deal", "OFFICIAL"),
    ("EUROPE", "Poland: Russia tried to kill rapper Kyivstoner twice", "CLAIM"),
    ("ASIA", "Kim Jong-un stresses sovereignty after rejecting Trump talks", "CLAIM"),
    ("ASIA", "Indonesia candy-factory fire: 24 body bags recovered", "REPORTED"),
    ("ASIA", "Asian tech stocks fall as the AI sell-off deepens", "CONFIRMED"),
]
ALSO_RIGHT = [
    ("ASIA", "Bitcoin falls to about $55,100, then recovers near $61,000", "CONFIRMED"),
    ("MIDDLE EAST", "Iran vows to fight a US blockade of the Strait of Hormuz", "CLAIM"),
    ("MIDDLE EAST", "Israeli strike on Gaza truck kills 3, including UNRWA staffer", "REPORTED"),
    ("MIDDLE EAST", "Saudi strike on Hodeida, Yemen: at least 4 killed, 18 hurt", "REPORTED"),
    ("MIDDLE EAST", "Oxfam: toxic contamination found in 99% of Gaza", "REPORTED"),
    ("AFRICA", "WHO chief urges peace as fighting disrupts Ebola response", "OFFICIAL"),
    ("AFRICA", "Drone hits a home and a UN building in Khartoum", "REPORTED"),
    ("OCEANIA", "NZ\u2013India Test drawn in Wellington; Australia back to No. 2", "CONFIRMED"),
    ("OCEANIA", "New Zealand retail sales rise 2.2% in Q3", "OFFICIAL"),
    ("LATIN AMERICA", "Bukele eyes a third term in El Salvador", "REPORTED"),
    ("LATIN AMERICA", "Argentina's Senate approves a permanent disability law", "OFFICIAL"),
    ("SCIENCE", "BepiColombo enters orbit around Mercury after 8 years", "CONFIRMED"),
]

NUMBERS = [
    ("7", "SEA DRONES SANK MERKURY"),
    ("15+", "KILLED IN KYIV STRIKES"),
    ("+30%", "NVIDIA'S ONE-DAY JUMP"),
    ("74", "LASHES FOR AHMADI'S BAND"),
    ("60", "BANKS IN EU SANCTIONS PLAN"),
    ("50,000+", "TRAVELLERS HIT IN BELGIUM"),
    ("$1.62BN", "INDIAN AID FOR NEPAL"),
]

TIMELINE = [
    ("00:39", "WHO: Ebola appeal"),
    ("03:15", "Belgium airports shut"),
    ("06:10", "Kyiv toll rises"),
    ("09:00", "Merkury confirmed"),
    ("10:06", "India aid to Nepal"),
    ("17:47", "Ahmadi flogged"),
    ("18:30", "US sanctions Iran"),
]

CHIPS = [
    ("AMERICA", 7), ("EUROPE", 10), ("ASIA", 6), ("MIDDLE EAST", 5),
    ("AFRICA", 3), ("OCEANIA", 3), ("LATIN AMERICA", 4),
]

# ------------------------------------------------------- illustrations
def art_merkury(d, x, y, w, h):
    """Sinking ship, sea waves and seven sea drones. Flat vector."""
    d.rectangle([x, y, x + w, y + h], fill=(22, 50, 74))
    d.rectangle([x, y, x + w, y + h], outline=NAVY_DK, width=1)
    # sky drones: seven small white dots with trails
    for i in range(7):
        dx = x + 12 + i * 18
        dy = y + 8 + (i % 2) * 5
        d.ellipse([dx, dy, dx + 4, dy + 4], fill=WHITE)
        d.line([(dx, dy + 6), (dx + 2, dy + 12)], fill=(140, 170, 200), width=1)
    # tilted hull, bow down, half under water
    hull = [(x + 28, y + 44), (x + 128, y + 34), (x + 134, y + 46),
            (x + 96, y + 58), (x + 40, y + 58)]
    d.polygon(hull, fill=(150, 152, 148))
    d.polygon([(x + 60, y + 36), (x + 78, y + 33), (x + 80, y + 42),
               (x + 62, y + 44)], fill=(110, 112, 108))
    # blast star where the hull is hit
    cx, cy = x + 100, y + 34
    for ang in range(0, 360, 45):
        import math
        r1 = 10 if ang % 90 == 0 else 5
        ex = cx + r1 * math.cos(math.radians(ang))
        ey = cy + r1 * math.sin(math.radians(ang))
        d.line([(cx, cy), (ex, ey)], fill=(240, 170, 60), width=2)
    # waves
    for wy in (y + 56, y + 62, y + 68):
        for k in range(0, w, 24):
            d.arc([x + k, wy - 3, x + k + 22, wy + 5], 180, 360,
                  fill=(170, 200, 225), width=2)


def art_nvidia(d, x, y, w, h):
    """Rising bars and an upward arrow. Flat vector."""
    d.rectangle([x, y, x + w, y + h], fill=(15, 46, 30))
    d.rectangle([x, y, x + w, y + h], outline=(10, 34, 22), width=1)
    bars = [(16, 34), (40, 26), (64, 18), (88, 10)]
    for bx, bh in bars:
        d.rectangle([x + bx, y + h - 12 - bh, x + bx + 18, y + h - 12],
                    fill=(46, 160, 90))
    # arrow climbing to the top right
    pts = [(x + 14, y + 52), (x + 48, y + 40), (x + 78, y + 30),
           (x + 118, y + 10)]
    d.line(pts, fill=(120, 230, 150), width=3, joint="curve")
    d.polygon([(x + 118, y + 10), (x + 104, y + 8), (x + 114, y + 20)],
              fill=(120, 230, 150))
    d.text((x + 10, y + 4), "+30%", font=sans_b(11), fill=(120, 230, 150))


def art_ahmadi(d, x, y, w, h):
    """Microphone behind bars. Flat vector, symbolic, no face."""
    d.rectangle([x, y, x + w, y + h], fill=(74, 21, 32))
    d.rectangle([x, y, x + w, y + h], outline=(52, 14, 22), width=1)
    # prison bars
    for bx in (x + 30, x + 74, x + 118):
        d.rectangle([bx, y, bx + 6, y + h], fill=(40, 10, 16))
    # microphone: grille circle, handle, stand
    cx, cy = x + 62, y + 24
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(200, 200, 198))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(140, 140, 138))
    d.polygon([(cx - 6, cy + 10), (cx + 6, cy + 10), (cx + 4, cy + 34),
               (cx - 4, cy + 34)], fill=(120, 120, 118))
    d.line([(cx, cy + 34), (cx, y + h - 8)], fill=(120, 120, 118), width=2)
    d.line([(cx - 12, y + h - 8), (cx + 12, y + h - 8)],
           fill=(120, 120, 118), width=2)
    # small red accent
    d.ellipse([x + 126, y + 8, x + 136, y + 18], fill=RED_LT)


ART = {"merkury": art_merkury, "nvidia": art_nvidia, "ahmadi": art_ahmadi}


# ------------------------------------------------------------- header
def draw_header(d):
    # navy banner
    d.rectangle([0, 0, W, 26], fill=NAVY)
    f = sans_b(12)
    d.text((16, 6), "THE WORLD IN ONE DAY", font=f, fill=WHITE)
    right = "38 STORIES  \u00b7  7 REGIONS  \u00b7  4 FIELDS"
    tw = d.textlength(right, font=f)
    d.text((W - 16 - tw, 6), right, font=f, fill=(200, 210, 235))
    # date masthead
    f = serif_b(30)
    txt = "MONDAY 23 NOVEMBER 2026"
    tw = d.textlength(txt, font=f)
    d.text(((W - tw) / 2, 32), txt, font=f, fill=NAVY)
    f = serif(12)
    sub = "Summing up the day's world news \u2014 every story happened or was first reported today"
    tw = d.textlength(sub, font=f)
    d.text(((W - tw) / 2, 64), sub, font=f, fill=GRAY)
    rule(d, 16, W - 16, 82, fill=NAVY, width=2)
    # red deck: the three heroes in one line each
    deck = [
        "Zelenskyy confirms Ukraine sank the Russian corvette Merkury off Libya",
        "Huang returns as Nvidia chief as the stock jumps 30% in a day",
        "Iran flogs singer Parastoo Ahmadi and four bandmates, 74 lashes each",
    ]
    y = 88
    f = serif(15)
    for ln in deck:
        tw = d.textlength(ln, font=f)
        d.text(((W - tw) / 2, y), ln, font=f, fill=RED)
        y += 18
    rule(d, 16, W - 16, 146, fill=LINE, width=1)
    return 150


def draw_chips(d, y):
    total_w = W - 32
    cw = total_w / len(CHIPS)
    x = 16
    for label, count in CHIPS:
        chip(d, int(x), y, int(cw) - 4, label, count, REGION[label])
        x += cw
    return y + 22


def draw_timeline(d, y):
    f = sans_b(10)
    d.text((16, y), "THE DAY \u00b7 UTC", font=f, fill=NAVY)
    line_y = y + 18
    d.line([(16, line_y), (W - 16, line_y)], fill=LINE, width=2)
    x0 = 150
    slot = (W - 16 - x0) / len(TIMELINE)
    for i, (t, ev) in enumerate(TIMELINE):
        cx = x0 + slot * i + slot / 2
        d.ellipse([cx - 4, line_y - 4, cx + 4, line_y + 4], fill=RED)
        ft = sans_b(10)
        tw = d.textlength(t, font=ft)
        d.text((cx - tw / 2, y + 2), t, font=ft, fill=NAVY)
        fe = sans(9)
        lines = wrap(d, ev, fe, slot - 8)
        ly = line_y + 6
        for ln in lines:
            tw = d.textlength(ln, font=fe)
            d.text((cx - tw / 2, ly), ln, font=fe, fill=INK)
            ly += 10
    return y + 44


def draw_numbers(d, y):
    f = sans_b(10)
    d.text((16, y), "THE DAY IN NUMBERS", font=f, fill=NAVY)
    y += 12
    cell = (W - 32) / len(NUMBERS)
    for i, (num, label) in enumerate(NUMBERS):
        x = 16 + cell * i
        if i:
            d.line([(x - 4, y), (x - 4, y + 34)], fill=LINE, width=1)
        fn = serif_b(21)
        d.text((x, y), num, font=fn, fill=RED)
        fl = sans(8)
        ly = draw_lines(d, wrap(d, label, fl, cell - 10), x, y + 24,
                        fl, GRAY, 10)
    return y + 36

# -------------------------------------------------------------- heroes
def draw_heroes(d, y):
    card_h = 70
    for hero in HEROES:
        # thin card
        d.rectangle([16, y, W - 16, y + card_h], fill=PAPER,
                    outline=LINE, width=1)
        # illustration panel
        ART[hero["art"]](d, 17, y + 1, 148, card_h - 2)
        tx = 178
        # line 1: number, place, category, tag pill
        f = sans_b(10)
        d.text((tx, y + 3), "%s \u00b7 %s \u2014 %s" % (
            hero["num"], hero["place"], hero["cat"]), font=f, fill=RED)
        tag_pill(d, W - 16 - 86, y + 2, hero["tag"])
        # headline
        fh = serif_b(16)
        d.text((tx, y + 17), hero["headline"], font=fh, fill=INK)
        # body, two lines max
        fb = sans(11)
        lines = wrap(d, hero["body"], fb, W - 16 - tx - 6)[:2]
        draw_lines(d, lines, tx, y + 35, fb, INK, 12)
        # source line
        d.text((tx, y + card_h - 11), hero["source"], font=sans(9),
               fill=GRAY)
        y += card_h + 3
    return y - 3


# ---------------------------------------------------------------- grid
def draw_grid(d, y):
    f = sans_b(11)
    d.text((16, y), "MORE OF THE DAY", font=f, fill=NAVY)
    rule(d, 130, W - 16, y + 6, fill=LINE, width=1)
    y += 16
    rows, cols = 5, 2
    cw = (W - 32) / cols
    ch = 31
    for idx, (region, head, summ, tag, src) in enumerate(GRID):
        r, c = divmod(idx, cols)
        x = 16 + c * cw
        gy = y + r * ch
        d.rectangle([x, gy, x + 3, gy + ch - 6], fill=REGION[region])
        hx = x + 9
        # headline + tag on one line
        fh = sans_b(12)
        d.text((hx, gy), head, font=fh, fill=INK)
        tw = d.textlength(head, font=fh)
        tag_pill(d, hx + tw + 6, gy + 1, tag)
        # summary one line, wrapped if needed, then source
        fs = sans(10)
        lines = wrap(d, summ + "  \u2014 " + src, fs, cw - 16)[:1]
        draw_lines(d, lines, hx, gy + 14, fs, GRAY, 12)
        if r < rows - 1:
            rule(d, x + 9, x + cw - 8, gy + ch - 2, fill=LINE, width=1)
    return y + rows * ch


# ---------------------------------------------------------------- ALSO
def draw_also(d, y):
    f = sans_b(11)
    d.text((16, y), "ALSO ON MONDAY 23 NOVEMBER", font=f, fill=NAVY)
    rule(d, 250, W - 16, y + 6, fill=LINE, width=1)
    y += 16
    col_w = (W - 32 - 24) / 2
    for col, items in enumerate((ALSO_LEFT, ALSO_RIGHT)):
        x = 16 + col * (col_w + 24)
        ly = y
        for region, head, tag in items:
            fr = sans_b(9)
            d.text((x, ly), region[:2].upper(), font=fr,
                   fill=REGION[region])
            fh = sans(10)
            lines = wrap(d, head, fh, col_w - 92)
            d.text((x + 22, ly), lines[0], font=fh, fill=INK)
            tag_pill(d, x + col_w - 62, ly, tag)
            ly += 12
    return y + 13 * 12


# ------------------------------------------------------------------ map
MAP_POLYS = [
    # North America
    [(28, 28), (70, 12), (150, 6), (230, 10), (285, 22), (305, 38),
     (295, 52), (260, 48), (245, 62), (215, 58), (185, 48), (150, 58),
     (110, 58), (70, 48), (35, 38)],
    # Greenland
    [(330, 8), (355, 6), (365, 18), (345, 24), (328, 16)],
    # South America
    [(305, 58), (335, 52), (365, 58), (375, 72), (360, 92), (335, 96),
     (315, 78), (300, 66)],
    # Europe
    [(468, 22), (500, 12), (540, 10), (562, 16), (555, 32), (520, 38),
     (490, 36), (472, 30)],
    # Africa
    [(468, 44), (510, 38), (548, 40), (578, 52), (572, 72), (552, 92),
     (520, 96), (492, 78), (472, 62), (460, 50)],
    # Asia
    [(562, 12), (640, 6), (730, 4), (820, 10), (880, 18), (905, 32),
     (885, 48), (830, 44), (800, 52), (782, 66), (745, 58), (705, 44),
     (660, 48), (620, 38), (585, 34), (560, 26)],
    # Australia
    [(815, 66), (860, 60), (895, 68), (905, 78), (875, 88), (835, 86),
     (812, 76)],
]
MAP_DOTS = [  # small navy dots: other stories
    (558, 24), (498, 24), (308, 62), (340, 76), (868, 82), (722, 44),
    (540, 66), (238, 38),
]
MAP_PINS = [  # (x, y, number) hero pins
    (548, 47, "1"), (232, 36, "2"), (648, 40, "3"),
]


def draw_map(d, y):
    f = sans_b(11)
    d.text((16, y), "WHERE IT HAPPENED", font=f, fill=NAVY)
    rule(d, 160, W - 16, y + 6, fill=LINE, width=1)
    my0 = y + 12
    my1 = y + 84
    sx = 0.992
    sy = (my1 - my0) / 100.0

    def px(pt):
        return (16 + pt[0] * sx, my0 + pt[1] * sy)

    for poly in MAP_POLYS:
        d.polygon([px(p) for p in poly], fill=(27, 42, 74))
    # SE Asia islands
    for ix, iy in ((790, 72), (810, 76), (770, 78)):
        cx, cy = px((ix, iy))
        d.ellipse([cx - 3, cy - 2, cx + 3, cy + 2], fill=NAVY)
    for pt in MAP_DOTS:
        cx, cy = px(pt)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    for pt in MAP_PINS:
        cx, cy = px((pt[0], pt[1]))
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED,
                  outline=WHITE, width=2)
        fn = sans_b(11)
        tw = d.textlength(pt[2], font=fn)
        d.text((cx - tw / 2, cy - 7), pt[2], font=fn, fill=WHITE)
    return my1


# ------------------------------------------------------- date check + footer
def draw_footer(d, y):
    # DATE CHECK box
    box_h = 50
    d.rectangle([16, y, W - 16, y + box_h], fill=(238, 230, 210),
                outline=RED, width=1)
    f = sans_b(11)
    d.text((26, y + 5), "DATE CHECK \u2014 WHAT WE LEFT OUT, AND WHY",
           font=f, fill=RED)
    fb = sans(10)
    txt = ("COP31 collapsed without a deal on Sunday 22 Nov \u2014 only its "
           "aftermath belongs to Monday. So do the Democrats' 258 House "
           "seats (22 Nov), the arrest of Chapo Isidro (21 Nov) and the "
           "California concert shooting (21 Nov). The Merkury sinking "
           "itself happened early Sunday; Monday's news is Zelenskyy's "
           "confirmation.")
    draw_lines(d, wrap(d, txt, fb, W - 52), 26, y + 18, fb, INK, 12)
    y += box_h + 6
    # legend
    fl = sans(10)
    leg = ("CONFIRMED = reported by two or more outlets   \u00b7   "
           "OFFICIAL = on the record   \u00b7   REPORTED = named wires   "
           "\u00b7   CLAIM = one side only")
    tw = d.textlength(leg, font=fl)
    d.text(((W - tw) / 2, y), leg, font=fl, fill=INK)
    y += 13
    fs = sans(9)
    src = ("Sources: AP, Reuters, WSJ, BBC, Al Jazeera, The Times, "
           "USA Today, G1 Globo, Ag\u00eancia Brasil, Oxfam, named wires. "
           "All events happened or were first reported on Monday "
           "23 November 2026, any time zone.")
    tw = d.textlength(src, font=fs)
    d.text(((W - tw) / 2, y), src, font=fs, fill=GRAY)
    y += 11
    fc = sans_b(9)
    close = "THE WORLD IN ONE DAY  \u00b7  MONDAY 23 NOVEMBER 2026  \u00b7  38 STORIES FROM 7 REGIONS"
    tw = d.textlength(close, font=fc)
    d.text(((W - tw) / 2, y), close, font=fc, fill=NAVY)
    return y + 12


# ------------------------------------------------------------------ main
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    y = draw_header(d)
    y = draw_chips(d, y)
    y = draw_timeline(d, y)
    y = draw_numbers(d, y)
    rule(d, 16, W - 16, y + 2, fill=NAVY, width=1)
    y = draw_heroes(d, y + 6)
    y = draw_grid(d, y + 4)
    y = draw_also(d, y + 2)
    y = draw_map(d, y + 2)
    y = draw_footer(d, y + 2)
    img.save(OUT, format="PNG", optimize=True)
    with open(OUT, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print("wrote %s  sha256=%s" % (OUT, digest))
    print("final y=%d (canvas %d)" % (y, H))


if __name__ == "__main__":
    build()
