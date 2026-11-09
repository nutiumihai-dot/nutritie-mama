"""Draws the app icon (Farfuria mea: a Horezu-style plate split into four food groups on a brown-red background) as PNGs without external libraries."""
import math
import struct
import sys
import zlib
from pathlib import Path


def draw(size):
    bg, cream, ochre = (110, 47, 23), (252, 244, 230), (213, 154, 42)
    quarters = ((94, 143, 53), (194, 85, 42), (213, 154, 42), (138, 63, 99))  # legume, proteine, cereale, fructe (clockwise from top-right)
    dots = [(50 + 29 * math.cos(2 * math.pi * k / 30), 50 + 29 * math.sin(2 * math.pi * k / 30)) for k in range(30)]
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
                    dx, dy = x - 50, y - 50
                    r = math.hypot(dx, dy)
                    c = bg
                    if r < 34:
                        c = cream
                        if any((x - ux) ** 2 + (y - uy) ** 2 < 1.5 ** 2 for ux, uy in dots):
                            c = ochre
                        if r < 22 and abs(dx) > 1.2 and abs(dy) > 1.2:
                            c = quarters[(0 if dx > 0 else 3) if dy < 0 else (1 if dx > 0 else 2)]
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
