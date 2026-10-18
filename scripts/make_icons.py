"""Create the two Fieldnotes app icons with Python's standard library."""

from pathlib import Path
import struct
import zlib


SITE = Path(__file__).resolve().parents[1] / "site"
BACKGROUND = (23, 111, 91)
LETTER = (255, 254, 250)
DOT = (169, 223, 198)


def color_at(x, y):
    # Keep the mark inside the center so Android can crop the icon safely.
    if (0.30 <= x <= 0.39 and 0.25 <= y <= 0.76) or (0.30 <= x <= 0.69 and 0.25 <= y <= 0.34) or (0.30 <= x <= 0.61 and 0.46 <= y <= 0.55):
        return LETTER
    if (x - 0.69) ** 2 + (y - 0.71) ** 2 <= 0.052 ** 2:
        return DOT
    return BACKGROUND


def chunk(kind, payload):
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff)


def make_icon(size):
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            row.extend(color_at((x + 0.5) / size, (y + 0.5) / size))
        rows.append(bytes(row))
    data = b"\x89PNG\r\n\x1a\n"
    data += chunk(b"IHDR", struct.pack(">2I5B", size, size, 8, 2, 0, 0, 0))
    data += chunk(b"IDAT", zlib.compress(b"".join(rows), level=9))
    data += chunk(b"IEND", b"")
    (SITE / f"icon-{size}.png").write_bytes(data)


if __name__ == "__main__":
    for dimension in (192, 512):
        make_icon(dimension)
    print("Created 192 and 512 pixel app icons.")
