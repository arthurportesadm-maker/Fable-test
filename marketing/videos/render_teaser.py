"""Render the Tracerail 35s teaser video programmatically.

v2 — motion-design pass: 1080p/30fps, eased motion everywhere (no linear),
a 2-second hook, kinetic typography, staggered terminal output with status
pills, an animated hash-chain tamper scene, and burned-in pacing for
silent autoplay feeds.

    pip install pillow imageio imageio-ffmpeg numpy
    python marketing/videos/render_teaser.py
"""

from __future__ import annotations

import math
import os

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30

# Brand palette (docs/BRAND.md)
BG = (11, 18, 32)          # #0B1220
SURFACE = (19, 28, 46)     # #131C2E
TEXT = (230, 237, 247)     # #E6EDF7
GREEN = (46, 230, 166)     # #2EE6A6
AMBER = (245, 184, 61)     # #F5B83D
RED = (229, 72, 77)        # #E5484D
DIM = (139, 152, 172)      # #8B98AC

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
MONO = os.path.join(FONT_DIR, "DejaVuSansMono.ttf")
MONO_BOLD = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")

_fonts: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


# --- easing ----------------------------------------------------------------

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def ease_out(x: float) -> float:
    """Cubic ease-out: fast start, gentle landing."""
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def ease_in_out(x: float) -> float:
    x = clamp01(x)
    return 3 * x * x - 2 * x * x * x


def overshoot(x: float, k: float = 1.70158) -> float:
    """Back ease-out: lands with a small, snappy overshoot."""
    x = clamp01(x) - 1
    return 1 + x * x * ((k + 1) * x + k)


def pulse(t: float, period: float = 1.1, lo: float = 0.55, hi: float = 1.0) -> float:
    return lo + (hi - lo) * (0.5 + 0.5 * math.sin(2 * math.pi * t / period))


def lerp(a, b, x):
    return a + (b - a) * x


def mix(c1, c2, x):
    return tuple(int(lerp(a, b, x)) for a, b in zip(c1, c2))


# --- drawing helpers --------------------------------------------------------

def blank() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    # vertical glow gradient keeps the dark frame from feeling flat
    top = ImageDraw.Draw(img)
    for y in range(0, H, 4):
        shade = int(10 * (1 - y / H))
        top.line([(0, y), (W, y)], fill=(BG[0] + shade, BG[1] + shade, BG[2] + shade + 4), width=4)
    return img


def vignette(img: Image.Image) -> Image.Image:
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-W * 0.25, -H * 0.35, W * 1.25, H * 1.35], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(180))
    black = Image.new("RGB", (W, H), (4, 8, 16))
    return Image.composite(img, black, mask)


def glow_text(img: Image.Image, pos, text, fnt, color, glow=0):
    """Text with an optional soft glow behind it."""
    if glow > 0:
        layer = Image.new("RGB", (W, H), (0, 0, 0))
        ImageDraw.Draw(layer).text(pos, text, font=fnt, fill=color)
        layer = layer.filter(ImageFilter.GaussianBlur(glow))
        img.paste(Image.blend(img, Image.new("RGB", (W, H), (0, 0, 0)), 0), (0, 0))
        arr = np.asarray(img).astype(np.int16) + np.asarray(layer).astype(np.int16) // 2
        img.paste(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)))
    ImageDraw.Draw(img).text(pos, text, font=fnt, fill=color)
    return img


def kinetic_line(img, words, y, t, t0, fnt, colors=None, stagger=0.09, rise=46):
    """Words pop in one by one: slide up + fade with ease-out."""
    draw = ImageDraw.Draw(img)
    widths = [draw.textlength(w + " ", font=fnt) for w in words]
    x = (W - sum(widths)) / 2
    for i, w in enumerate(words):
        p = ease_out((t - t0 - i * stagger) / 0.32)
        if p > 0:
            color = (colors or [TEXT] * len(words))[i]
            faded = mix(BG, color, p)
            draw.text((x, y + (1 - p) * rise), w, font=fnt, fill=faded)
        x += widths[i]
    return img


def chain_block(draw, x, y, s, fill, outline, check=False, w=4):
    draw.rounded_rectangle([x, y, x + s, y + s], radius=s * 0.22, fill=fill, outline=outline, width=w)
    if check:
        draw.line([x + s * 0.26, y + s * 0.54, x + s * 0.44, y + s * 0.72], fill=BG, width=int(s * 0.12))
        draw.line([x + s * 0.44, y + s * 0.72, x + s * 0.78, y + s * 0.30], fill=BG, width=int(s * 0.12))


def draw_logo(img, t, t0, cx, cy, scale=1.0):
    """Chain blocks assemble one by one with overshoot, then the check pops."""
    draw = ImageDraw.Draw(img)
    s = 64 * scale
    gap = 26 * scale
    base = [(cx - 1.5 * (s + gap), cy + (s + gap) * 0.8),
            (cx - 0.5 * (s + gap), cy),
            (cx + 0.5 * (s + gap), cy - (s + gap) * 0.8)]
    for i, (bx, by) in enumerate(base):
        p = overshoot((t - t0 - i * 0.18) / 0.45)
        if p <= 0:
            continue
        size = s * p
        ox, oy = bx + (s - size) / 2, by + (s - size) / 2
        last = i == 2
        chain_block(draw, ox, oy, size, GREEN if last else SURFACE,
                    GREEN if last else DIM, check=last and p > 0.75, w=max(3, int(5 * scale)))
        if i > 0 and p > 0.5:  # link draws toward the previous block
            px, py = base[i - 1]
            lp = ease_out((p - 0.5) / 0.5)
            x1, y1 = px + s, py + s / 2
            x2, y2 = bx, by + s / 2
            draw.line([x1, y1, x1 + (x2 - x1) * lp, y1 + (y2 - y1) * lp], fill=DIM, width=max(3, int(5 * scale)))
    return img


# --- scenes -----------------------------------------------------------------

def scene_hook(t: float) -> Image.Image:
    """0-2.4s — the $9,999 counter slams in. Hook for silent feeds."""
    img = blank()
    draw = ImageDraw.Draw(img)
    p = ease_out(t / 0.9)
    amount = int(9999 * p)
    fnt = font(SANS_BOLD, 230)
    txt = f"${amount:,}"
    tw = draw.textlength(txt, font=fnt)
    flash = max(0.0, 1 - t / 0.5)
    color = mix(TEXT, RED, 0.35 + 0.65 * min(1.0, t / 0.9) + flash * 0)
    draw.text(((W - tw) / 2, H * 0.26), txt, font=fnt, fill=color)
    kinetic_line(img, "Your AI agent just refunded this.".split(), H * 0.62, t, 0.7,
                 font(SANS_BOLD, 64))
    return img


def scene_question(t: float) -> Image.Image:
    """Agitate: nobody approved it / could you prove it?"""
    img = blank()
    kinetic_line(img, "Nobody approved it.".split(), H * 0.34, t, 0.0,
                 font(SANS_BOLD, 88), colors=[AMBER] * 3)
    kinetic_line(img, "Could you prove what happened?".split(), H * 0.52, t, 0.85,
                 font(SANS_BOLD, 64), colors=[TEXT] * 5)
    return img


def scene_logo_intro(t: float) -> Image.Image:
    img = blank()
    draw_logo(img, t, 0.0, W / 2, H * 0.30, scale=1.15)
    draw = ImageDraw.Draw(img)
    p = ease_out((t - 0.7) / 0.4)
    if p > 0:
        fnt = font(MONO_BOLD, 110)
        tw = draw.textlength("tracerail", font=fnt)
        draw.text(((W - tw) / 2, H * 0.52 + (1 - p) * 40), "tracerail", font=fnt, fill=mix(BG, TEXT, p))
    p2 = ease_out((t - 1.15) / 0.4)
    if p2 > 0:
        fnt = font(SANS_BOLD, 44)
        sub = "The control plane for AI agent actions"
        tw = draw.textlength(sub, font=fnt)
        draw.text(((W - tw) / 2, H * 0.68), sub, font=fnt, fill=mix(BG, DIM, p2))
    return img


TERM_EVENTS = [
    ("cmd", "tracerail proxy --policies policies.yaml -- npx payments-server", None),
    ("out", "[tracerail] session 7f3a guarding: npx payments-server", DIM, None),
    ("call", "issue_refund  amount: $40", "ALLOW", GREEN),
    ("call", "db_query      env: prod", "DENY", RED),
    ("call", "issue_refund  amount: $9,999", "HELD", AMBER),
    ("cmd", "tracerail approve 588d3411 --by alice", None),
    ("call", "issue_refund  amount: $9,999", "APPROVED", GREEN),
    ("cmd", "tracerail verify", None),
    ("out", "OK: audit chain intact (8 records)", GREEN, None),
]

TYPE_CPS = 52
HOLD = 1.6


def term_schedule():
    t, sched = 0.5, []
    for ev in TERM_EVENTS:
        if ev[0] == "cmd":
            dur = len(ev[1]) / TYPE_CPS
            sched.append((t, dur))
            t += dur + 0.38
        else:
            t += 0.42
            sched.append((t, 0.0))
            t += 0.14
    return sched, t + HOLD


def scene_terminal(t: float, sched) -> Image.Image:
    img = blank()
    draw = ImageDraw.Draw(img)
    m, top = 170, 120
    # window with soft drop shadow
    shadow = Image.new("RGB", (W, H), BG)
    ImageDraw.Draw(shadow).rounded_rectangle([m + 14, top + 20, W - m + 14, H - 120 + 20],
                                             radius=24, fill=(4, 8, 16))
    img = Image.blend(img, shadow, 0.5)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([m, top, W - m, H - 120], radius=24, fill=SURFACE, outline=(34, 48, 74), width=3)
    for i, c in enumerate((RED, AMBER, GREEN)):
        draw.ellipse([m + 36 + i * 40, top + 30, m + 60 + i * 40, top + 54], fill=c)
    draw.text((W / 2 - 90, top + 28), "tracerail", font=font(MONO, 28), fill=DIM)

    mono, mono_b = font(MONO, 32), font(MONO_BOLD, 32)
    pill_f = font(MONO_BOLD, 27)
    x, y, line_h = m + 54, top + 110, 56
    for ev, (start, dur) in zip(TERM_EVENTS, sched):
        if t < start:
            break
        appear = ease_out((t - start) / 0.3)
        kind = ev[0]
        if kind == "cmd":
            shown = ev[1][: int(max(0.0, t - start) * TYPE_CPS)] if t < start + dur else ev[1]
            draw.text((x, y), "$", font=mono_b, fill=GREEN)
            draw.text((x + 44, y), shown, font=mono, fill=TEXT)
            if t < start + dur + 0.25 and int(t * 3) % 2 == 0:
                cx = x + 44 + draw.textlength(shown, font=mono)
                draw.rectangle([cx + 4, y + 4, cx + 22, y + 36], fill=TEXT)
        elif kind == "out":
            draw.text((x + (1 - appear) * 60, y), ev[1], font=mono, fill=mix(SURFACE, ev[2], appear))
        else:  # call row with a status pill sliding in
            _, label, status, color = ev
            draw.text((x + 10 + (1 - appear) * 60, y), label, font=mono, fill=mix(SURFACE, TEXT, appear))
            pw = draw.textlength(status, font=pill_f) + 44
            px = W - m - 70 - pw + (1 - appear) * 90
            hot = 1.0 if status != "HELD" else pulse(t, 0.9, 0.55, 1.0)
            fill = mix(SURFACE, color, 0.22 * appear * hot)
            draw.rounded_rectangle([px, y - 4, px + pw, y + 44], radius=22,
                                   fill=fill, outline=mix(SURFACE, color, appear * hot), width=3)
            draw.text((px + 22, y + 3), status, font=pill_f, fill=mix(SURFACE, color, appear))
        y += line_h
    return img


def scene_chain(t: float) -> Image.Image:
    """Five hash-linked blocks; one gets tampered, the chain snaps red."""
    img = blank()
    draw = ImageDraw.Draw(img)
    kinetic_line(img, "Every record carries the hash of the last.".split(), H * 0.16, t, 0.0,
                 font(SANS_BOLD, 56))
    s, gap = 130, 96
    total = 5 * s + 4 * gap
    x0, cy = (W - total) / 2, H * 0.46
    tamper_at = 2.3
    for i in range(5):
        p = overshoot((t - 0.25 - i * 0.16) / 0.4)
        if p <= 0:
            continue
        bx = x0 + i * (s + gap)
        tampered = i == 2 and t > tamper_at
        glitch = (math.sin(53 * t) * 6) if (tampered and t < tamper_at + 0.5) else 0
        color = RED if tampered else SURFACE
        outline = RED if tampered else (GREEN if t > 0.25 + i * 0.16 + 0.5 else DIM)
        size = s * min(1.0, p)
        chain_block(draw, bx + (s - size) / 2 + glitch, cy + (s - size) / 2, size,
                    color, outline, check=not tampered and p > 0.8, w=6)
        if i > 0 and p > 0.4:
            lx1 = x0 + (i - 1) * (s + gap) + s
            broken = i in (2, 3) and t > tamper_at
            draw.line([lx1 + 8, cy + s / 2, bx - 8, cy + s / 2],
                      fill=RED if broken else GREEN, width=6)
            if broken:
                mxp = (lx1 + bx) / 2
                draw.line([mxp - 14, cy + s / 2 - 22, mxp + 14, cy + s / 2 + 22], fill=BG, width=18)
    if t > tamper_at + 0.4:
        kinetic_line(img, "Tamper with history — the chain breaks.".split(), H * 0.70,
                     t, tamper_at + 0.4, font(SANS_BOLD, 60),
                     colors=[TEXT, TEXT, TEXT, RED, RED, RED, RED])
    if t > tamper_at + 1.3:
        kinetic_line(img, "Instantly detected.".split(), H * 0.80, t, tamper_at + 1.3,
                     font(SANS_BOLD, 54), colors=[GREEN, GREEN])
    return img


def scene_value(t: float) -> Image.Image:
    img = blank()
    rows = [("Policies.", TEXT, 0.0), ("Approvals.", AMBER, 0.35), ("Tamper-evident audit.", GREEN, 0.7)]
    for text, color, t0 in rows:
        kinetic_line(img, [text], H * 0.28 + rows.index((text, color, t0)) * 130, t, t0,
                     font(SANS_BOLD, 92), colors=[color])
    kinetic_line(img, "Drop-in MCP proxy. Zero agent code changes.".split(), H * 0.72, t, 1.2,
                 font(MONO, 42), colors=[DIM] * 7)
    return img


def scene_outro(t: float) -> Image.Image:
    img = blank()
    draw_logo(img, t, 0.0, W / 2, H * 0.24, scale=0.95)
    draw = ImageDraw.Draw(img)
    p = ease_out((t - 0.55) / 0.4)
    if p > 0:
        fnt = font(MONO_BOLD, 96)
        tw = draw.textlength("tracerail", font=fnt)
        draw.text(((W - tw) / 2, H * 0.44), "tracerail", font=fnt, fill=mix(BG, TEXT, p))
    p2 = ease_out((t - 0.95) / 0.4)
    if p2 > 0:
        fnt = font(SANS_BOLD, 46)
        tag = "Every agent action, accounted for."
        tw = draw.textlength(tag, font=fnt)
        draw.text(((W - tw) / 2, H * 0.58), tag, font=fnt, fill=mix(BG, DIM, p2))
    p3 = ease_out((t - 1.35) / 0.4)
    if p3 > 0:  # pulsing CTA pill
        fnt = font(MONO_BOLD, 40)
        cta = "github.com/tracerail/tracerail"
        tw = draw.textlength(cta, font=fnt)
        px, py, pad = (W - tw) / 2, H * 0.72, 36
        hot = pulse(t, 1.4, 0.6, 1.0) * p3
        draw.rounded_rectangle([px - pad, py - 18, px + tw + pad, py + 64], radius=42,
                               fill=mix(BG, GREEN, 0.16 * hot), outline=mix(BG, GREEN, hot), width=4)
        draw.text((px, py), cta, font=fnt, fill=mix(BG, GREEN, max(p3, 0.7)))
        sub = "Open source - Apache-2.0"
        sf = font(MONO, 30)
        sw = draw.textlength(sub, font=sf)
        draw.text(((W - sw) / 2, py + 110), sub, font=sf, fill=mix(BG, DIM, p3))
    return img


# --- timeline ---------------------------------------------------------------

def build_timeline():
    sched, term_dur = term_schedule()
    return [
        (2.4, scene_hook),
        (2.6, scene_question),
        (2.6, scene_logo_intro),
        (term_dur, lambda t: scene_terminal(t, sched)),
        (4.6, scene_chain),
        (3.0, scene_value),
        (3.6, scene_outro),
    ]


FADE = 0.30


def main() -> None:
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "teaser-30s.mp4")
    writer = imageio.get_writer(out_path, fps=FPS, codec="libx264", quality=8,
                                ffmpeg_params=["-pix_fmt", "yuv420p"])
    total = 0.0
    for duration, scene in build_timeline():
        for i in range(int(duration * FPS)):
            t = i / FPS
            frame = vignette(scene(t))
            alpha = min(1.0, t / FADE, (duration - t) / FADE)
            if alpha < 1.0:
                frame = Image.blend(Image.new("RGB", (W, H), (4, 8, 16)), frame, alpha)
            writer.append_data(np.asarray(frame))
        total += duration
    writer.close()
    print(f"wrote {out_path} ({total:.1f}s, {int(total * FPS)} frames, {W}x{H}@{FPS}fps)")


if __name__ == "__main__":
    main()
