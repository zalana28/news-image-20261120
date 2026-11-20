#!/usr/bin/env python3
"""Compose the news-image-20261120 front page: one 1024x1024 PNG.

Layout (all fresh design, drawn with PIL):
  masthead + dateline, hero photo strip carrying the lead story (ICJ verdict),
  a 2x2 grid of four stories, a full-width navy strip for GTA 6, footer.
Deterministic: no timestamps, no randomness, fixed fonts and text.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.expanduser("~/workspace/fonts")

W, H = 1024, 1024
PAPER = (247, 242, 232)      # warm newsprint
CARD = (255, 253, 247)       # story card
INK = (20, 24, 31)
NAVY = (20, 38, 74)
GOLD = (185, 138, 47)
RULE = (216, 205, 184)
MUTED = (90, 86, 76)
WHITE = (255, 255, 255)

RED = (158, 43, 37)
AMBER = (138, 109, 27)
TEAL = (31, 92, 90)
GREEN = (46, 107, 52)
PURPLE = (91, 58, 142)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


F_MAST = font("PlayfairDisplay-Bold.ttf", 56)
F_DATE = font("PlusJakartaSans-Bold.ttf", 19)
F_LEAD = font("PlusJakartaSans-Bold.ttf", 33)
F_SUB = font("PlusJakartaSans-Regular.ttf", 19)
F_TAG = font("PlusJakartaSans-Bold.ttf", 15)
F_HEAD = font("PlusJakartaSans-Bold.ttf", 23)
F_BODY = font("PlusJakartaSans-Regular.ttf", 17)
F_STRIP_HEAD = font("PlusJakartaSans-Bold.ttf", 30)
F_STRIP_BODY = font("PlusJakartaSans-Regular.ttf", 18)
F_FOOT = font("PlusJakartaSans-Regular.ttf", 13)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_tag(draw, x, y, label, color):
    """Solid tag chip; returns width used."""
    pad_x, pad_y = 10, 5
    tw = draw.textlength(label, font=F_TAG)
    w, h = int(tw) + 2 * pad_x, 26
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=color)
    draw.text((x + pad_x, y + pad_y - 1), label, font=F_TAG, fill=WHITE)
    return w


def story_card(draw, box, tag, tag_color, headline, body):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6,
                           fill=CARD, outline=RULE, width=1)
    draw_tag(draw, x0 + 14, y0 + 12, tag, tag_color)
    tx = x0 + 14
    tw = x1 - x0 - 28
    hy = y0 + 48
    for line in wrap(draw, headline, F_HEAD, tw)[:2]:
        draw.text((tx, hy), line, font=F_HEAD, fill=INK)
        hy += 28
    by = hy + 6
    for line in wrap(draw, body, F_BODY, tw)[:3]:
        draw.text((tx, by), line, font=F_BODY, fill=(52, 50, 46))
        by += 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top rules + masthead ---
    d.rectangle([0, 0, W, 5], fill=GOLD)
    d.rectangle([0, 8, W, 10], fill=NAVY)
    title = "THE WORLD IN ONE PAGE"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, 20), title, font=F_MAST, fill=NAVY)

    # --- dateline row ---
    d.line([36, 100, 988, 100], fill=RULE, width=1)
    d.text((36, 110), "FRIDAY, 20 NOVEMBER 2026", font=F_DATE, fill=INK)
    right = "SIX STORIES  ·  ONE DAY"
    d.text((988 - d.textlength(right, font=F_DATE), 110), right,
           font=F_DATE, fill=INK)
    d.line([36, 138, 988, 138], fill=RULE, width=1)

    # --- hero strip with lead story ---
    hero = Image.open(os.path.join(HERE, "assets", "hero.png")).convert("RGB")
    hw, hh = 952, 210
    scaled = hero.resize((hw, int(hero.height * hw / hero.width)),
                         Image.LANCZOS)
    top = (scaled.height - hh) // 2
    strip = scaled.crop((0, top, hw, top + hh))
    img.paste(strip, (36, 150))
    d.rectangle([36, 150, 988, 360], outline=RULE, width=1)

    # gradient shade at the bottom of the hero for the lead headline
    shade = Image.new("RGBA", (hw, 92), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for i in range(92):
        a = int(215 * (i / 91) ** 1.4)
        sd.line([(0, i), (hw, i)], fill=(10, 14, 22, a))
    img.paste(shade, (36, 360 - 92), shade)
    d = ImageDraw.Draw(img)
    draw_tag(d, 50, 162, "THE HAGUE  ·  JUSTICE", NAVY)
    d.text((50, 290), "WORLD COURT: MYANMAR COMMITTED GENOCIDE",
           font=F_LEAD, fill=WHITE)
    d.text((50, 328), "The Hague rules 9–6 — a first against a state — over the Rohingya.",
           font=F_SUB, fill=(235, 230, 220))

    # --- 2x2 story grid ---
    col_w, row_h, gap = 464, 190, 24
    y_grid = 376
    stories = [
        ("KYIV  ·  WAR", RED,
         "Russia's barrage hits Kyiv bridges; missiles land in Poland",
         "Eight killed and 28 hurt in the war's biggest air assault; three Dnipro "
         "crossings struck. Two missiles and a drone came down in Poland — NATO jets scrambled."),
        ("RIYADH  ·  GULF", AMBER,
         "Houthi missile scars Riyadh's tallest tower",
         "The PIF Tower's windows blew out across seven floors; no one was hurt. "
         "On Friday, Saudi defences shot down a missile and five drones."),
        ("SHENZHEN  ·  BERLIN", TEAL,
         "After the trilateral, Europe demands its seat",
         "Trump, Xi and Putin signed a four-point declaration — but no breakthrough "
         "on Ukraine. In Berlin, 37 allies said no peace over their heads."),
        ("NEW YORK  ·  MARKETS", GREEN,
         "Anthropic closes up 17% after record IPO",
         "Shares ended at $97.17 after opening at $111.50; the $81.3bn listing is "
         "the biggest ever. Stocks fell for a fifth straight day."),
    ]
    for i, (tag, color, head, body) in enumerate(stories):
        cx = 36 + (i % 2) * (col_w + gap)
        cy = y_grid + (i // 2) * (row_h + 12)
        story_card(d, (cx, cy, cx + col_w, cy + row_h), tag, color, head, body)

    # --- full-width navy strip: GTA 6 ---
    sy = 784
    d.rounded_rectangle([36, sy, 988, sy + 132], radius=6, fill=NAVY)
    d.rectangle([36, sy, 44, sy + 132], fill=GOLD)
    draw_tag(d, 60, sy + 12, "GAMES  ·  RECORDS", PURPLE)
    d.text((60, sy + 44), "GTA 6: $2.36 BILLION IN A DAY",
           font=F_STRIP_HEAD, fill=WHITE)
    d.text((60, sy + 84),
           "An estimated 24.6 million copies sold in 24 hours — the biggest entertainment",
           font=F_STRIP_BODY, fill=(225, 222, 214))
    d.text((60, sy + 108),
           "launch on record, Sensor Tower estimates; Take-Two has yet to confirm the figures.",
           font=F_STRIP_BODY, fill=(225, 222, 214))

    # --- footer ---
    d.line([36, 932, 988, 932], fill=RULE, width=1)
    foot = ("All events of Friday 20 November 2026  ·  Sources: Reuters, The Times, WSJ, AP, "
            "Barron's, CNN, Sensor Tower (estimates)")
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, 946), foot, font=F_FOOT, fill=MUTED)
    d.text(((W - d.textlength("news-image-20261120", font=F_FOOT)) / 2, 966),
           "news-image-20261120", font=F_FOOT, fill=MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
