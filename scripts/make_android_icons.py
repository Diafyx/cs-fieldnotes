"""Make Android launcher icons from the website icon design."""

from pathlib import Path
import math
import struct
import zlib

from make_icons import chunk, color_at


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "android" / "app" / "src" / "main" / "res" / "drawable-nodpi"


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    size = 512
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            center_x = (x + 0.5) / size
            center_y = (y + 0.5) / size
            distance = math.hypot(center_x - 0.5, center_y - 0.5)
            alpha = round(255 * max(0.0, min(1.0, (0.48 - distance) * size)))
            row.extend((*color_at(center_x, center_y), alpha))
        rows.append(bytes(row))
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">2I5B", size, size, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(b"".join(rows), level=9))
    png += chunk(b"IEND", b"")
    (DEST / "app_icon.png").write_bytes(png)


if __name__ == "__main__":
    main()
