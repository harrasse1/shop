"""
Minimal pure-Python PDF writer (no external dependencies).
Supports:
 - Multiple pages (auto wrap, auto pagination)
 - Helvetica + Helvetica-Bold + Helvetica-Oblique
 - WinAnsiEncoding (covers French accented characters)
 - Simple line-based text layout with paragraphs and headings
"""

from __future__ import annotations
import zlib
from typing import List


# --- WinAnsiEncoding helpers --------------------------------------------------

# Standard 14 PDF fonts use WinAnsiEncoding (close to CP1252) when explicitly
# requested.  Encoding the text in CP1252 lets accented French characters
# render correctly without needing to embed a TrueType font.
def _enc(text: str) -> bytes:
    # Replace characters not present in CP1252 with a sensible fallback so we
    # never crash on stray Unicode (e.g. en/em-dashes, smart quotes).
    replacements = {
        "\u2013": "-",   # en dash
        "\u2014": "-",   # em dash
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2026": "...", # ellipsis
        "\u00a0": " ",   # non-breaking space
        "\u00d7": "x",   # multiplication sign -> ascii x
        "\u00f7": "/",   # division sign
        "\u2192": "->",  # right arrow
        "\u2190": "<-",
        "\u2194": "<->",
        "\u21d2": "=>",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u2260": "!=",
        "\u00b1": "+/-",
        "\u00d7": "x",
        "\u2640": "(F)",     # female sign
        "\u2642": "(M)",     # male sign
        "\u2248": "~",       # approximately equal
        "\u00b7": "-",       # middle dot
        "\u25cf": "o",       # black circle
        "\u25cb": "o",       # white circle
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode("cp1252", errors="replace")


def _escape_pdf_string(b: bytes) -> bytes:
    return (
        b.replace(b"\\", b"\\\\")
         .replace(b"(", b"\\(")
         .replace(b")", b"\\)")
    )


# --- Font metric tables (Adobe AFM core widths) -------------------------------
# Width tables for the standard core fonts (in 1/1000 em units).
# We embed only the WinAnsi-relevant range so we can wrap text accurately.
# These numbers come from the Adobe Core 14 AFM specification (public domain).

_HELV_WIDTHS = {
    32: 278, 33: 278, 34: 355, 35: 556, 36: 556, 37: 889, 38: 667, 39: 191,
    40: 333, 41: 333, 42: 389, 43: 584, 44: 278, 45: 333, 46: 278, 47: 278,
    48: 556, 49: 556, 50: 556, 51: 556, 52: 556, 53: 556, 54: 556, 55: 556,
    56: 556, 57: 556, 58: 278, 59: 278, 60: 584, 61: 584, 62: 584, 63: 556,
    64: 1015, 65: 667, 66: 667, 67: 722, 68: 722, 69: 667, 70: 611, 71: 778,
    72: 722, 73: 278, 74: 500, 75: 667, 76: 556, 77: 833, 78: 722, 79: 778,
    80: 667, 81: 778, 82: 722, 83: 667, 84: 611, 85: 722, 86: 667, 87: 944,
    88: 667, 89: 667, 90: 611, 91: 278, 92: 278, 93: 278, 94: 469, 95: 556,
    96: 222, 97: 556, 98: 556, 99: 500, 100: 556, 101: 556, 102: 278, 103: 556,
    104: 556, 105: 222, 106: 222, 107: 500, 108: 222, 109: 833, 110: 556,
    111: 556, 112: 556, 113: 556, 114: 333, 115: 500, 116: 278, 117: 556,
    118: 500, 119: 722, 120: 500, 121: 500, 122: 500, 123: 334, 124: 260,
    125: 334, 126: 584,
    # WinAnsi extras (roughly accurate enough for layout)
    160: 278, 161: 333, 162: 556, 163: 556, 164: 556, 165: 556, 166: 260,
    167: 556, 168: 333, 169: 737, 170: 370, 171: 556, 172: 584, 173: 333,
    174: 737, 175: 333, 176: 400, 177: 584, 178: 333, 179: 333, 180: 333,
    181: 556, 182: 537, 183: 278, 184: 333, 185: 333, 186: 365, 187: 556,
    188: 834, 189: 834, 190: 834, 191: 611,
    192: 667, 193: 667, 194: 667, 195: 667, 196: 667, 197: 667, 198: 1000,
    199: 722, 200: 667, 201: 667, 202: 667, 203: 667, 204: 278, 205: 278,
    206: 278, 207: 278, 208: 722, 209: 722, 210: 778, 211: 778, 212: 778,
    213: 778, 214: 778, 215: 584, 216: 778, 217: 722, 218: 722, 219: 722,
    220: 722, 221: 667, 222: 667, 223: 611,
    224: 556, 225: 556, 226: 556, 227: 556, 228: 556, 229: 556, 230: 889,
    231: 500, 232: 556, 233: 556, 234: 556, 235: 556, 236: 278, 237: 278,
    238: 278, 239: 278, 240: 556, 241: 556, 242: 556, 243: 556, 244: 556,
    245: 556, 246: 556, 247: 584, 248: 611, 249: 556, 250: 556, 251: 556,
    252: 556, 253: 500, 254: 556, 255: 500,
}

_HELVB_WIDTHS = {
    32: 278, 33: 333, 34: 474, 35: 556, 36: 556, 37: 889, 38: 722, 39: 238,
    40: 333, 41: 333, 42: 389, 43: 584, 44: 278, 45: 333, 46: 278, 47: 278,
    48: 556, 49: 556, 50: 556, 51: 556, 52: 556, 53: 556, 54: 556, 55: 556,
    56: 556, 57: 556, 58: 333, 59: 333, 60: 584, 61: 584, 62: 584, 63: 611,
    64: 975, 65: 722, 66: 722, 67: 722, 68: 722, 69: 667, 70: 611, 71: 778,
    72: 722, 73: 278, 74: 556, 75: 722, 76: 611, 77: 833, 78: 722, 79: 778,
    80: 667, 81: 778, 82: 722, 83: 667, 84: 611, 85: 722, 86: 667, 87: 944,
    88: 667, 89: 667, 90: 611, 91: 333, 92: 278, 93: 333, 94: 584, 95: 556,
    96: 278, 97: 556, 98: 611, 99: 556, 100: 611, 101: 556, 102: 333, 103: 611,
    104: 611, 105: 278, 106: 278, 107: 556, 108: 278, 109: 889, 110: 611,
    111: 611, 112: 611, 113: 611, 114: 389, 115: 556, 116: 333, 117: 611,
    118: 556, 119: 778, 120: 556, 121: 556, 122: 500, 123: 389, 124: 280,
    125: 389, 126: 584,
    160: 278, 161: 333, 162: 556, 163: 556, 164: 556, 165: 556, 166: 280,
    167: 556, 168: 333, 169: 737, 170: 370, 171: 556, 172: 584, 173: 333,
    174: 737, 175: 333, 176: 400, 177: 584, 178: 333, 179: 333, 180: 333,
    181: 611, 182: 556, 183: 278, 184: 333, 185: 333, 186: 365, 187: 556,
    188: 834, 189: 834, 190: 834, 191: 611,
    192: 722, 193: 722, 194: 722, 195: 722, 196: 722, 197: 722, 198: 1000,
    199: 722, 200: 667, 201: 667, 202: 667, 203: 667, 204: 278, 205: 278,
    206: 278, 207: 278, 208: 722, 209: 722, 210: 778, 211: 778, 212: 778,
    213: 778, 214: 778, 215: 584, 216: 778, 217: 722, 218: 722, 219: 722,
    220: 722, 221: 667, 222: 667, 223: 611,
    224: 556, 225: 556, 226: 556, 227: 556, 228: 556, 229: 556, 230: 889,
    231: 556, 232: 556, 233: 556, 234: 556, 235: 556, 236: 278, 237: 278,
    238: 278, 239: 278, 240: 611, 241: 611, 242: 611, 243: 611, 244: 611,
    245: 611, 246: 611, 247: 584, 248: 611, 249: 611, 250: 611, 251: 611,
    252: 611, 253: 556, 254: 611, 255: 556,
}


def _string_width(text_bytes: bytes, font: str, size: float) -> float:
    table = _HELVB_WIDTHS if font.endswith("B") else _HELV_WIDTHS
    total = 0
    for b in text_bytes:
        total += table.get(b, 500)
    return total * size / 1000.0


# --- Document ---------------------------------------------------------------

class PDF:
    PAGE_W = 595  # A4 width in PDF points (72 dpi)
    PAGE_H = 842  # A4 height
    MARGIN_L = 54
    MARGIN_R = 54
    MARGIN_T = 54
    MARGIN_B = 60

    def __init__(self) -> None:
        self.pages: List[List[bytes]] = []  # list of content-stream chunks per page
        self.cur_page: List[bytes] = []
        self.pages.append(self.cur_page)
        self.y = self.PAGE_H - self.MARGIN_T
        self.default_size = 11
        self.line_gap = 1.35  # leading multiplier
        self._title = "Document"

    # ---------- low-level drawing helpers ----------
    def _emit_text(self, text: str, x: float, y: float, font: str, size: float) -> None:
        eb = _escape_pdf_string(_enc(text))
        chunk = b"BT /%s %s Tf %s %s Td (" % (
            font.encode(),
            f"{size}".encode(),
            f"{x:.2f}".encode(),
            f"{y:.2f}".encode(),
        ) + eb + b") Tj ET\n"
        self.cur_page.append(chunk)

    def _new_page(self) -> None:
        self.cur_page = []
        self.pages.append(self.cur_page)
        self.y = self.PAGE_H - self.MARGIN_T

    def _ensure_room(self, height: float) -> None:
        if self.y - height < self.MARGIN_B:
            self._new_page()

    # ---------- public layout API ----------
    def set_title(self, title: str) -> None:
        self._title = title

    def hr(self, gap: float = 6) -> None:
        """Horizontal rule."""
        self._ensure_room(gap + 2)
        x1 = self.MARGIN_L
        x2 = self.PAGE_W - self.MARGIN_R
        y = self.y - gap / 2
        self.cur_page.append(
            f"0.6 w 0.6 0.6 0.6 RG {x1:.2f} {y:.2f} m {x2:.2f} {y:.2f} l S\n".encode()
        )
        self.y -= gap

    def space(self, h: float = 6) -> None:
        self.y -= h
        if self.y < self.MARGIN_B:
            self._new_page()

    def heading(self, text: str, level: int = 1) -> None:
        sizes = {1: 18, 2: 14, 3: 12}
        size = sizes.get(level, 12)
        self._ensure_room(size * self.line_gap + 6)
        self.y -= size  # baseline drop
        self._emit_text(text, self.MARGIN_L, self.y, "F2", size)
        self.y -= size * 0.45
        if level == 1:
            self.hr(8)

    def paragraph(self, text: str, size: float | None = None,
                  font: str = "F1", indent: float = 0) -> None:
        if size is None:
            size = self.default_size
        max_width = self.PAGE_W - self.MARGIN_L - self.MARGIN_R - indent
        words = text.split(" ")
        line: List[str] = []
        line_w = 0.0
        space_w = _string_width(_enc(" "), font, size)
        for w in words:
            ww = _string_width(_enc(w), font, size)
            need = ww if not line else line_w + space_w + ww
            if need > max_width and line:
                self._draw_line(" ".join(line), font, size, indent)
                line = [w]
                line_w = ww
            else:
                if line:
                    line_w += space_w + ww
                else:
                    line_w = ww
                line.append(w)
        if line:
            self._draw_line(" ".join(line), font, size, indent)

    def _draw_line(self, line: str, font: str, size: float, indent: float) -> None:
        h = size * self.line_gap
        self._ensure_room(h)
        self.y -= size
        self._emit_text(line, self.MARGIN_L + indent, self.y, font, size)
        self.y -= (h - size)

    def bullet(self, text: str, size: float | None = None) -> None:
        if size is None:
            size = self.default_size
        # Draw bullet then paragraph indented
        self._ensure_room(size * self.line_gap)
        self.y -= size
        self._emit_text("\u2022", self.MARGIN_L + 6, self.y, "F1", size)
        # restore y so paragraph re-decrements consistently
        self.y += size
        self.paragraph(text, size=size, indent=20)

    def code(self, text: str, size: float = 10) -> None:
        # Monospace-like rendering using Courier (F3)
        for ln in text.splitlines():
            h = size * self.line_gap
            self._ensure_room(h)
            self.y -= size
            self._emit_text(ln, self.MARGIN_L + 8, self.y, "F3", size)
            self.y -= (h - size)

    def boxed(self, text: str, size: float | None = None) -> None:
        """Draw a one-line important fact in bold, indented."""
        if size is None:
            size = self.default_size
        self.paragraph(text, size=size, font="F2", indent=12)

    # ---------- output ----------
    def build(self) -> bytes:
        # Build PDF objects
        objects: List[bytes] = []

        def add(obj_bytes: bytes) -> int:
            objects.append(obj_bytes)
            return len(objects)

        # Allocate object numbers in deterministic order:
        #  1: Catalog
        #  2: Pages
        #  3: F1 (Helvetica)
        #  4: F2 (Helvetica-Bold)
        #  5: F3 (Courier)
        #  6..N: Page + Content for each page
        # We'll fill them all then concat.

        n_pages = len(self.pages)
        first_page_obj = 6
        page_obj_ids = []
        content_obj_ids = []
        for i in range(n_pages):
            page_obj_ids.append(first_page_obj + 2 * i)
            content_obj_ids.append(first_page_obj + 2 * i + 1)

        # Catalog
        catalog = b"<< /Type /Catalog /Pages 2 0 R >>"
        # Pages
        kids = b" ".join(f"{pid} 0 R".encode() for pid in page_obj_ids)
        pages = (
            b"<< /Type /Pages /Count " + str(n_pages).encode() +
            b" /Kids [" + kids + b"] >>"
        )
        # Fonts (use WinAnsiEncoding for accented characters)
        f1 = (b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
              b"/Encoding /WinAnsiEncoding >>")
        f2 = (b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold "
              b"/Encoding /WinAnsiEncoding >>")
        f3 = (b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier "
              b"/Encoding /WinAnsiEncoding >>")

        add(catalog)  # 1
        add(pages)    # 2
        add(f1)       # 3
        add(f2)       # 4
        add(f3)       # 5

        # Pages and their content streams
        for i, page_chunks in enumerate(self.pages):
            content_id = content_obj_ids[i]
            page_id = page_obj_ids[i]
            # Compose content stream
            stream = b"".join(page_chunks)
            compressed = zlib.compress(stream)
            content_obj = (
                b"<< /Length " + str(len(compressed)).encode() +
                b" /Filter /FlateDecode >>\nstream\n" + compressed + b"\nendstream"
            )
            page_obj = (
                b"<< /Type /Page /Parent 2 0 R "
                b"/MediaBox [0 0 " + str(self.PAGE_W).encode() + b" " + str(self.PAGE_H).encode() + b"] "
                b"/Contents " + str(content_id).encode() + b" 0 R "
                b"/Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R >> >> >>"
            )
            # Place at right indices; use placeholders so order stays correct
            # We must keep numbering aligned; objects list grows in order.
            # Insert page_obj first, then content_obj? No, both numbers are predetermined.
            # We'll just append in order page_id then content_id.
            objects.append(page_obj)
            objects.append(content_obj)

        # Now serialize
        out = bytearray()
        out += b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"  # binary marker for binary-safe readers
        offsets = [0]  # offsets[0] is unused
        for i, obj in enumerate(objects, start=1):
            offsets.append(len(out))
            out += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"

        xref_pos = len(out)
        out += f"xref\n0 {len(objects)+1}\n".encode()
        out += b"0000000000 65535 f \n"
        for off in offsets[1:]:
            out += f"{off:010d} 00000 n \n".encode()

        # Trailer
        title_enc = _escape_pdf_string(_enc(self._title))
        info = (b"<< /Title (" + title_enc + b") /Producer (Kiro pure-python pdf) >>")
        objects.append(info)
        # Append info as a real object so /Info reference works
        info_id = len(objects)
        offsets.append(len(out))
        out += f"{info_id} 0 obj\n".encode() + info + b"\nendobj\n"

        # Rewrite xref to include the info object
        xref_pos = len(out)
        out += f"xref\n0 {len(objects)+1}\n".encode()
        out += b"0000000000 65535 f \n"
        for off in offsets[1:]:
            out += f"{off:010d} 00000 n \n".encode()

        out += (
            b"trailer\n<< /Size " + str(len(objects)+1).encode() +
            b" /Root 1 0 R /Info " + str(info_id).encode() + b" 0 R >>\n" +
            b"startxref\n" + str(xref_pos).encode() + b"\n%%EOF\n"
        )
        return bytes(out)

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            f.write(self.build())
