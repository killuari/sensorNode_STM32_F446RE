#!/usr/bin/env python3
"""Generates docs/images/wiring_diagram.svg (Fritzing-style breadboard view).

The diagram mirrors the netlist of the real build shown in
docs/images/hardware_setup.jpg, but with a tidied-up layout and
conventional wire colours (red = 3V3, black = GND, yellow = SCL, blue = SDA).

Run:  python3 docs/generate_wiring_diagram.py
"""

from pathlib import Path

# ---------------------------------------------------------------- geometry --
W, H = 1280, 720

# breadboard
BB_X, BB_Y = 400, 150
COLS = 30
PITCH = 26
BB_W = COLS * PITCH + 2 * PITCH
RAIL_TOP = [BB_Y + 26, BB_Y + 52]          # + and - holes (top rail group)
ROWS_AE = [BB_Y + 108 + i * PITCH for i in range(5)]   # a..e
GAP = ROWS_AE[-1] + 22
ROWS_FJ = [GAP + 26 + i * PITCH for i in range(5)]     # f..j
RAIL_BOT = [ROWS_FJ[-1] + 34, ROWS_FJ[-1] + 60]
BB_H = RAIL_BOT[-1] + 26 - BB_Y

# nucleo
NU_X, NU_Y, NU_W, NU_H = 60, 190, 250, 400

# colours
C_3V3, C_GND, C_SCL, C_SDA = "#d0342c", "#2b2b2b", "#e0a800", "#2f6fdb"
BOARD_BG = "#f4f2ec"


def col_x(c: int) -> float:
    """x coordinate of breadboard column c (1..COLS)."""
    return BB_X + PITCH + (c - 1) * PITCH


out: list[str] = []
add = out.append

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="DejaVu Sans, Verdana, sans-serif">')
add('<defs>'
    '<filter id="sh" x="-20%" y="-20%" width="150%" height="150%">'
    '<feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.25"/></filter>'
    '</defs>')
add(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')

# ------------------------------------------------------------------ title --
add(f'<text x="{W/2}" y="46" text-anchor="middle" font-size="26" font-weight="bold" '
    f'fill="#1b1b1b">STM32 Environmental Sensor Node &#8212; Wiring Diagram</text>')
add(f'<text x="{W/2}" y="72" text-anchor="middle" font-size="15" fill="#555">'
    f'NUCLEO-F446RE &#183; BME280 &#183; SSD1306/SH1106 OLED &#183; shared I&#178;C1 bus '
    f'(PB8 = SCL, PB9 = SDA) @ 3.3 V</text>')

# --------------------------------------------------------------- nucleo ----
add(f'<g filter="url(#sh)"><rect x="{NU_X}" y="{NU_Y}" width="{NU_W}" height="{NU_H}" '
    f'rx="10" fill="#fbfbfb" stroke="#c9c9c9" stroke-width="2"/></g>')
add(f'<rect x="{NU_X+34}" y="{NU_Y+186}" width="96" height="96" rx="4" fill="#5a5148"/>')
add(f'<text x="{NU_X+82}" y="{NU_Y+240}" text-anchor="middle" font-size="12" '
    f'fill="#fff">STM32F446</text>')
add(f'<text x="{NU_X+NU_W/2}" y="{NU_Y+34}" text-anchor="middle" font-size="17" '
    f'font-weight="bold" fill="#0b3d91">NUCLEO-F446RE</text>')
add(f'<text x="{NU_X+NU_W/2}" y="{NU_Y+54}" text-anchor="middle" font-size="12" '
    f'fill="#777">powered via ST-LINK USB</text>')
add(f'<rect x="{NU_X+12}" y="{NU_Y+90}" width="14" height="270" rx="3" fill="#2a2a2a"/>')

# right hand pin block (the four signals we actually use)
PINS = [
    ("+3V3",        "CN6-4",       C_3V3),
    ("GND",         "CN6-6",       C_GND),
    ("PB8 / D15",   "CN10-3 (SCL)", C_SCL),
    ("PB9 / D14",   "CN10-5 (SDA)", C_SDA),
]
pin_y = {}
add(f'<rect x="{NU_X+NU_W-26}" y="{NU_Y+90}" width="14" height="270" rx="3" fill="#2a2a2a"/>')
for i, (name, hdr, col) in enumerate(PINS):
    y = NU_Y + 120 + i * 62
    pin_y[name] = y
    add(f'<rect x="{NU_X+NU_W-26}" y="{y-9}" width="14" height="18" rx="2" fill="{col}"/>')
    add(f'<text x="{NU_X+NU_W-36}" y="{y-2}" text-anchor="end" font-size="14" '
        f'font-weight="bold" fill="#1b1b1b">{name}</text>')
    add(f'<text x="{NU_X+NU_W-36}" y="{y+13}" text-anchor="end" font-size="11" '
        f'fill="#777">{hdr}</text>')

# ------------------------------------------------------------ breadboard ---
add(f'<g filter="url(#sh)"><rect x="{BB_X}" y="{BB_Y}" width="{BB_W}" height="{BB_H}" '
    f'rx="8" fill="{BOARD_BG}" stroke="#d8d4c8" stroke-width="2"/></g>')
# rail marker lines
for y, c, lbl in ((RAIL_TOP[0] - 14, C_3V3, "+"), (RAIL_TOP[1] + 14, "#3a6fd8", "−"),
                  (RAIL_BOT[0] - 14, C_3V3, "+"), (RAIL_BOT[1] + 14, "#3a6fd8", "−")):
    add(f'<line x1="{BB_X+18}" y1="{y}" x2="{BB_X+BB_W-18}" y2="{y}" '
        f'stroke="{c}" stroke-width="1.6" opacity="0.75"/>')
    add(f'<text x="{BB_X+8}" y="{y+5}" font-size="15" fill="{c}">{lbl}</text>')
# centre channel
add(f'<rect x="{BB_X+4}" y="{ROWS_AE[-1]+11}" width="{BB_W-8}" height="{ROWS_FJ[0]-ROWS_AE[-1]-22}" '
    f'fill="#e6e2d8"/>')

def holes(rows, cols_range, group=5):
    for y in rows:
        for c in cols_range:
            x = col_x(c)
            add(f'<rect x="{x-4.5}" y="{y-4.5}" width="9" height="9" rx="1.5" fill="#3d3d3d"/>')

holes(ROWS_AE, range(1, COLS + 1))
holes(ROWS_FJ, range(1, COLS + 1))
for y in RAIL_TOP + RAIL_BOT:
    for c in range(1, COLS + 1):
        if c % 6 == 0:      # rail groups of five with a gap
            continue
        x = col_x(c)
        add(f'<rect x="{x-4.5}" y="{y-4.5}" width="9" height="9" rx="1.5" fill="#3d3d3d"/>')
# row letters / column numbers
for i, ch in enumerate("abcde"):
    add(f'<text x="{BB_X+BB_W-14}" y="{ROWS_AE[i]+4}" font-size="10" fill="#9a968c">{ch}</text>')
for i, ch in enumerate("fghij"):
    add(f'<text x="{BB_X+BB_W-14}" y="{ROWS_FJ[i]+4}" font-size="10" fill="#9a968c">{ch}</text>')
for c in []:  # column numbers omitted (kept clean)
    add(f'<text x="{col_x(c)}" y="{ROWS_AE[0]-14}" text-anchor="middle" font-size="10" '
        f'fill="#9a968c">{c}</text>')


# ------------------------------------------------------------- modules -----
OLED_C0, BME_C0 = 4, 23          # first pin column of each module
SCL_COL, SDA_COL = 13, 18        # bus nodes carrying the pull-ups
ROW_SCL, ROW_SDA = ROWS_AE[2], ROWS_AE[3]     # rows c and d carry the bus


def module(c0, width_pad, height, body, title, pins, label_dy=26):
    x = col_x(c0) - width_pad
    w = 3 * PITCH + 2 * width_pad
    y = ROWS_AE[-1] + 16
    add(f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{height}" '
        f'rx="6" fill="{body[0]}" stroke="{body[1]}" stroke-width="2"/></g>')
    for i, (lbl, col) in enumerate(pins):
        px = col_x(c0 + i)
        add(f'<circle cx="{px}" cy="{ROWS_AE[-1]}" r="5.5" fill="#c9a227" stroke="#8a6d0f"/>')
        add(f'<text x="{px}" y="{ROWS_AE[-1]-11}" text-anchor="middle" font-size="10" '
            f'font-weight="bold" fill="{col}">{lbl}</text>')
    add(f'<text x="{x+w/2}" y="{y+height-10}" text-anchor="middle" font-size="11.5" '
        f'font-weight="bold" fill="{body[2]}">{title}</text>')
    return x, y, w


# OLED
ox, oy, ow = module(OLED_C0, 34, 150, ("#1d3f7a", "#16305c", "#cfe0ff"),
                    'SSD1306 &#183; 0x3C',
                    (("VDD", C_3V3), ("GND", C_GND), ("SCK", C_SCL), ("SDA", C_SDA)))
add(f'<rect x="{ox+14}" y="{oy+16}" width="{ow-28}" height="100" rx="3" fill="#0a0a12"/>')
for i, line in enumerate(("Temp: 27.9 C", "Pres: 958.9 hPa", "Hum:  46.4 %")):
    add(f'<text x="{ox+ow/2}" y="{oy+46+i*24}" text-anchor="middle" font-size="13" '
        f'fill="#dfe7ff" font-family="DejaVu Sans Mono, monospace">{line}</text>')

# BME280
bx, by, bw = module(BME_C0, 30, 120, ("#141414", "#000000", "#dcdcdc"),
                    'BME280 &#183; 0x76',
                    (("VCC", C_3V3), ("GND", C_GND), ("SCL", C_SCL), ("SDA", C_SDA)))
add(f'<rect x="{bx+bw/2-17}" y="{by+34}" width="34" height="28" rx="3" fill="#9a9a9a"/>')
add(f'<circle cx="{bx+bw/2}" cy="{by+48}" r="7" fill="#6f6f6f"/>')
add(f'<text x="{bx+bw/2}" y="{by+84}" text-anchor="middle" font-size="12" fill="#e6e6e6">BME280</text>')

# ---------------------------------------------------------------- wires ----
def wire(pts, colour, width=4.2, dots=True):
    d = f'M {pts[0][0]} {pts[0][1]}' + "".join(f' L {x} {y}' for x, y in pts[1:])
    add(f'<path d="{d}" fill="none" stroke="#00000020" stroke-width="{width+2.5}" '
        f'stroke-linecap="round" stroke-linejoin="round"/>')
    add(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round"/>')
    if dots:
        for x, y in (pts[0], pts[-1]):
            add(f'<circle cx="{x}" cy="{y}" r="3.6" fill="#242424"/>')


def node(x, y):
    add(f'<circle cx="{x}" cy="{y}" r="4.6" fill="#242424"/>')


NX = NU_X + NU_W - 12            # x where the nucleo pins leave the board

# --- power: nucleo -> top rails
wire([(NX, pin_y["+3V3"]), (BB_X - 30, pin_y["+3V3"]), (BB_X - 30, RAIL_TOP[0]),
      (col_x(1), RAIL_TOP[0])], C_3V3)
wire([(NX, pin_y["GND"]), (BB_X - 52, pin_y["GND"]), (BB_X - 52, RAIL_TOP[1]),
      (col_x(2), RAIL_TOP[1])], C_GND)

# --- I2C: nucleo -> bus rows
wire([(NX, pin_y["PB8 / D15"]), (BB_X - 74, pin_y["PB8 / D15"]), (BB_X - 74, ROW_SCL),
      (col_x(SCL_COL), ROW_SCL)], C_SCL)
wire([(NX, pin_y["PB9 / D14"]), (BB_X - 96, pin_y["PB9 / D14"]), (BB_X - 96, ROW_SDA),
      (col_x(SDA_COL), ROW_SDA)], C_SDA)

# --- bus jumpers to the modules (drawn along rows c / d)
wire([(col_x(OLED_C0 + 2), ROW_SCL), (col_x(SCL_COL), ROW_SCL)], C_SCL)
wire([(col_x(SCL_COL), ROW_SCL), (col_x(BME_C0 + 2), ROW_SCL)], C_SCL)
wire([(col_x(OLED_C0 + 3), ROW_SDA), (col_x(SDA_COL), ROW_SDA)], C_SDA)
wire([(col_x(SDA_COL), ROW_SDA), (col_x(BME_C0 + 3), ROW_SDA)], C_SDA)
node(col_x(SCL_COL), ROW_SCL)
node(col_x(SDA_COL), ROW_SDA)

# --- power taps for both modules (row a/b -> rails)
for c0 in (OLED_C0, BME_C0):
    wire([(col_x(c0), ROWS_AE[1]), (col_x(c0), RAIL_TOP[0])], C_3V3, 3.6)
    wire([(col_x(c0 + 1), ROWS_AE[0]), (col_x(c0 + 1), RAIL_TOP[1])], C_GND, 3.6)

# ------------------------------------------------------------- resistors ---
def resistor(col, y_bottom, label, side=1):
    x = col_x(col)
    y_top = RAIL_TOP[0]
    add(f'<line x1="{x}" y1="{y_bottom}" x2="{x}" y2="{y_top}" stroke="#a8a8a8" stroke-width="2.4"/>')
    cy = (y_bottom + y_top) / 2 + 2
    add(f'<rect x="{x-8}" y="{cy-21}" width="16" height="42" rx="7" fill="#e6d7a6" stroke="#c3b285"/>')
    for i, c in enumerate(("#7a4a1e", "#111111", "#c0392b", "#c9a227")):
        add(f'<rect x="{x-8}" y="{cy-15+i*8.5}" width="16" height="4.5" fill="{c}"/>')
    add(f'<circle cx="{x}" cy="{y_bottom}" r="3.6" fill="#242424"/>')
    add(f'<circle cx="{x}" cy="{y_top}" r="3.6" fill="#242424"/>')
    tx = x + 24 * side
    anchor = "start" if side > 0 else "end"
    add(f'<text x="{tx}" y="{cy+4}" text-anchor="{anchor}" font-size="11.5" '
        f'font-weight="bold" fill="#3a3a3a" stroke="#ffffff" stroke-width="3.5" '
        f'paint-order="stroke" stroke-linejoin="round">{label}</text>')


resistor(SCL_COL, ROW_SCL, "4.7 k&#8486;", -1)
resistor(SDA_COL, ROW_SDA, "4.7 k&#8486;", 1)

# ---------------------------------------------------------------- legend ---
LX, LY = BB_X, BB_Y + BB_H + 26
add(f'<rect x="{LX}" y="{LY}" width="{BB_W}" height="86" rx="6" fill="#fafafa" stroke="#e6e6e6"/>')
for i, (lbl, col) in enumerate((("3.3 V", C_3V3), ("GND", C_GND),
                                ("SCL &#8212; PB8 / D15", C_SCL), ("SDA &#8212; PB9 / D14", C_SDA))):
    x = LX + 24 + i * 196
    add(f'<line x1="{x}" y1="{LY+26}" x2="{x+32}" y2="{LY+26}" stroke="{col}" '
        f'stroke-width="4.2" stroke-linecap="round"/>')
    add(f'<text x="{x+40}" y="{LY+30}" font-size="13" fill="#333">{lbl}</text>')
add(f'<text x="{LX+24}" y="{LY+54}" font-size="12" fill="#666">'
    f'Both modules share one I&#178;C1 bus. A wire drawn along a row is the jumper tying those '
    f'breadboard columns together.</text>')
add(f'<text x="{LX+24}" y="{LY+70}" font-size="12" fill="#666">'
    f'The two 4.7 k&#8486; resistors pull SCL and SDA up to the +3.3 V rail.</text>')

add('</svg>')

target = Path(__file__).resolve().parent / "images" / "wiring_diagram.svg"
target.write_text("\n".join(out), encoding="utf-8")
print(f"wrote {target}")
