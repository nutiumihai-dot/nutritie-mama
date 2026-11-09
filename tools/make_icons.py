"""Draws the app icon (sage background, warm bowl, two leaves) as PNGs without external libraries."""
import struct
import sys
import zlib
from pathlib import Path


def draw(size):
    bg_top, bg_bot = (78, 112, 88), (52, 82, 62)
    bowl, rim, leaf, leaf2, vein = (232, 140, 94), (246, 214, 190), (168, 214, 150), (120, 186, 120), (60, 110, 70)
    ss = 3
    rows = []
    for py in range(size):
        row = bytearray([0])
        for px in range(size):
            acc = [0, 0, 0]
            for sy in range(ss):
                for sx in range(ss):
                    x = (px + (sx + .5) / ss) * 100 / size
                    y = (py + (sy + .5) / ss) * 100 / size
                    t = y / 100
                    c = tuple(round(bg_top[i] + (bg_bot[i] - bg_top[i]) * t) for i in range(3))
                    # leaves: two ellipses tilted, above the bowl (inside the maskable safe zone)
                    for cx, cy, ang, col in ((42, 40, -0.6, leaf), (58, 38, 0.6, leaf2)):
                        import math
                        dx, dy = x - cx, y - cy
                        u = dx * math.cos(ang) + dy * math.sin(ang)
                        v = -dx * math.sin(ang) + dy * math.cos(ang)
                        if (u / 6.5) ** 2 + (v / 14) ** 2 < 1:
                            c = vein if abs(u) < 0.6 else col
                    # bowl: lower half-disc with a rim
                    if 52 <= y <= 56 and 20 <= x <= 80:
                        c = rim
                    elif y > 56 and (x - 50) ** 2 + ((y - 56) * 1.35) ** 2 < 30 ** 2:
                        c = bowl
                    if 77 <= y <= 81 and 40 <= x <= 60:
                        c = bowl
                    for i in range(3):
                        acc[i] += c[i]
            row += bytes(round(v / ss / ss) for v in acc)
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


out = Path(sys.argv[1])
for s in (192, 512):
    (out / f"icon-{s}.png").write_bytes(draw(s))
print("ok")
