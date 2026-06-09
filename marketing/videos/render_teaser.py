"""Render the Tracerail 30s teaser video programmatically.

Produces marketing/videos/teaser-30s.mp4 (1280x720, 24fps) using only
Pillow + imageio, so the asset can be regenerated after any copy or
brand tweak without a video editor:

    pip install pillow imageio imageio-ffmpeg
    python marketing/videos/render_teaser.py
"""

from __future__ import annotations

import os

import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 24

# Brand palette (docs/BRAND.md)
BG = "#0B1220"
SURFACE = "#131C2E"
TEXT = "#E6EDF7"
GREEN = "#2EE6A6"
AMBER = "#F5B83D"
RED = "#E5484D"
DIM = "#8B98AC"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
MONO = os.path.join(FONT_DIR, "DejaVuSansMono.ttf")
MONO_BOLD = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def blank() -> Image.Image:
    return Image.new("RGB", (W, H), BG)


def fade(img: Image.Image, alpha: float) -> Image.Image:
    """Fade a frame from/to the background color."""
    if alpha >= 1.0:
        return img
    return Image.blend(blank(), img, max(0.0, alpha))


def draw_icon(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0) -> None:
    """Three chained blocks rising diagonally; last one green with a check."""
    s = int(34 * scale)
    gap = int(14 * scale)
    blocks = [(x, y + 2 * (s + gap) - 40), (x + s + gap, y + (s + gap) - 20), (x + 2 * (s + gap), y)]
    for i, (bx, by) in enumerate(blocks):
        color = GREEN if i == 2 else SURFACE
        outline = GREEN if i == 2 else DIM
        draw.rounded_rectangle([bx, by, bx + s, by + s], radius=int(8 * scale), fill=color, outline=outline, width=2)
        if i < 2:  # chain link to the next block
            nx, ny = blocks[i + 1]
            draw.line([bx + s, by + s // 2, nx, ny + s // 2], fill=DIM, width=3)
    bx, by = blocks[2]  # check mark on the green block
    draw.line([bx + s * 0.25, by + s * 0.52, bx + s * 0.43, by + s * 0.72], fill=BG, width=int(5 * scale))
    draw.line([bx + s * 0.43, by + s * 0.72, bx + s * 0.78, by + s * 0.30], fill=BG, width=int(5 * scale))


def card(lines: list[tuple[str, str, int]], icon: bool = False) -> Image.Image:
    """Centered title card: list of (text, color, font_size)."""
    img = blank()
    draw = ImageDraw.Draw(img)
    rendered = [(t, c, font(SANS_BOLD if s >= 40 else MONO, s)) for t, c, s in lines]
    total = sum(f.size + 26 for _, _, f in rendered)
    y = (H - total) // 2 + (40 if icon else 0)
    if icon:
        draw_icon(draw, W // 2 - 70, y - 170, 1.2)
    for text, color, fnt in rendered:
        tw = draw.textlength(text, font=fnt)
        draw.text(((W - tw) // 2, y), text, font=fnt, fill=color)
        y += fnt.size + 26
    return img


# --- terminal scene -------------------------------------------------------

# (kind, text, color) — kind: "cmd" is typed char by char, "out" appears at once
SCRIPT = [
    ("cmd", "tracerail proxy --policies policies.yaml -- npx payments-server", TEXT),
    ("out", "[tracerail] session 7f3a guarding: npx payments-server", DIM),
    ("out", "", DIM),
    ("out", "  issue_refund {\"amount\": 40}            ALLOW   refund-cap", GREEN),
    ("out", "  db_query     {\"env\": \"prod\"}            DENY    block-prod-db", RED),
    ("out", "  issue_refund {\"amount\": 9999}          HELD    awaiting approval", AMBER),
    ("out", "", DIM),
    ("cmd", "tracerail approve 588d3411 --by alice", TEXT),
    ("out", "588d3411 approved: issue_refund          ALLOW   approved by human", GREEN),
    ("out", "", DIM),
    ("cmd", "tracerail verify", TEXT),
    ("out", "OK: audit chain intact (8 records)", GREEN),
]

TYPE_CPS = 38        # typed characters per second
OUT_DELAY = 0.55     # pause before an output line appears
END_HOLD = 2.2       # hold the finished terminal on screen


def terminal_schedule() -> tuple[list[tuple[float, float]], float]:
    """Start time and typing duration for each script line."""
    t, sched = 0.6, []
    for kind, text, _ in SCRIPT:
        if kind == "cmd":
            dur = len(text) / TYPE_CPS
            sched.append((t, dur))
            t += dur + 0.45
        else:
            t += OUT_DELAY
            sched.append((t, 0.0))
            t += 0.12
    return sched, t + END_HOLD


def terminal_frame(t: float, sched: list[tuple[float, float]]) -> Image.Image:
    img = blank()
    draw = ImageDraw.Draw(img)
    margin, top = 90, 80
    draw.rounded_rectangle([margin, top, W - margin, H - 90], radius=14, fill=SURFACE, outline="#22304A", width=2)
    for i, c in enumerate(("#E5484D", "#F5B83D", "#2EE6A6")):  # window dots
        draw.ellipse([margin + 24 + i * 26, top + 20, margin + 40 + i * 26, top + 36], fill=c)
    title_f = font(MONO, 18)
    draw.text((W // 2 - 60, top + 18), "tracerail", font=title_f, fill=DIM)

    mono = font(MONO, 21)
    mono_b = font(MONO_BOLD, 21)
    x, y, line_h = margin + 34, top + 64, 34
    for (kind, text, color), (start, dur) in zip(SCRIPT, sched):
        if t < start:
            break
        if kind == "cmd":
            shown = text[: int(max(0.0, t - start) * TYPE_CPS)] if t < start + dur else text
            draw.text((x, y), "$ ", font=mono_b, fill=GREEN)
            draw.text((x + 28, y), shown, font=mono, fill=color)
            if t < start + dur + 0.3:  # block cursor while typing
                cx = x + 28 + draw.textlength(shown, font=mono)
                draw.rectangle([cx + 2, y + 2, cx + 14, y + 24], fill=TEXT)
        else:
            draw.text((x, y), text, font=mono, fill=color)
        y += line_h
    return img


# --- timeline -------------------------------------------------------------

def build_timeline():
    sched, term_dur = terminal_schedule()
    scenes = [
        (3.2, lambda t: card([("tracerail", TEXT, 64), ("Every agent action, accounted for.", DIM, 26)], icon=True)),
        (3.4, lambda t: card([("Your AI agents take real actions.", TEXT, 48),
                              ("Refunds. Emails. Deploys.", DIM, 30)])),
        (2.8, lambda t: card([("Can you prove what they did?", AMBER, 48)])),
        (term_dur, lambda t: terminal_frame(t, sched)),
        (3.2, lambda t: card([("Policies. Approvals.", TEXT, 50),
                              ("Tamper-evident audit.", GREEN, 50),
                              ("Open source - Apache-2.0", DIM, 26)])),
        (3.4, lambda t: card([("tracerail", TEXT, 64),
                              ("github.com/tracerail/tracerail", GREEN, 30),
                              ("Every agent action, accounted for.", DIM, 24)], icon=True)),
    ]
    return scenes


FADE = 0.45  # seconds of fade in/out per scene


def main() -> None:
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "teaser-30s.mp4")
    writer = imageio.get_writer(out_path, fps=FPS, codec="libx264", quality=8,
                                ffmpeg_params=["-pix_fmt", "yuv420p"])
    total = 0.0
    for duration, scene in build_timeline():
        frames = int(duration * FPS)
        for i in range(frames):
            t = i / FPS
            alpha = min(1.0, t / FADE, (duration - t) / FADE)
            writer.append_data(__import__("numpy").asarray(fade(scene(t), alpha)))
        total += duration
    writer.close()
    print(f"wrote {out_path} ({total:.1f}s, {int(total * FPS)} frames)")


if __name__ == "__main__":
    main()
