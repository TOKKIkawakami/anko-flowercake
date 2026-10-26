"""Wilton 口金 #103・#104 セット告知リール 1080x1920 / 約13秒。

使い方: python3 reel/make_nozzle_reel.py → reel/tokki_nozzle_set_reel.mp4
"""
import math

from make_reel import (ANKO, CARD103, CARD104, PINK, ROOT, W, WHITE, brand,
                       ease_back, ease_out, paste, pill, render, text)

OUT = ROOT / "reel" / "tokki_nozzle_set_reel.mp4"
LABEL = "Wilton 口金セット"


def scene_hook(base, d, t):
    a1 = ease_out(t / 0.4)
    text(d, (W / 2, 680 - 40 * (1 - a1)), "Wilton口金", 96, ANKO, alpha=a1, base=base)
    text(d, (W / 2, 810 - 40 * (1 - a1)), "どこにも売ってない…", 84, ANKO, alpha=a1, base=base)
    a2 = ease_back((t - 0.8) / 0.45)
    if a2 > 0:
        pill(base, W / 2, 1060, 820 * min(1, a2), 190, PINK)
        if a2 > 0.6:
            text(d, (W / 2, 1060), "TOKKIにあります！", 80, WHITE)


def scene_set(base, d, t):
    brand(base, d, LABEL)
    a = ease_out(t / 0.4)
    text(d, (W / 2, 400), "103番と104番を", 76, ANKO, alpha=a, base=base)
    text(d, (W / 2, 500), "1個ずつセットでお届け", 76, ANKO, alpha=a, base=base)
    for i, c in enumerate((CARD103, CARD104)):
        s = ease_back((t - 0.3 - i * 0.25) / 0.5)
        if s > 0:
            paste(base, c, W / 2, 800 + i * 380, scale=0.55 * (0.7 + 0.3 * s), alpha=min(1, s))
    a2 = ease_out((t - 1.0) / 0.4)
    if a2 > 0:
        text(d, (W / 2, 1420), "小花・つぼみも、大きなバラも", 50, PINK, alpha=a2, base=base)


def scene_ship(base, d, t):
    brand(base, d, LABEL)
    a = ease_out(t / 0.4)
    text(d, (W / 2, 700), "口金だけのご注文は", 80, ANKO, alpha=a, base=base)
    a2 = ease_back((t - 0.5) / 0.45)
    if a2 > 0:
        pill(base, W / 2, 900, 860 * min(1, a2), 200, PINK)
        if a2 > 0.6:
            text(d, (W / 2, 900), "送料お安くしました", 80, WHITE)
    a3 = ease_out((t - 1.1) / 0.4)
    if a3 > 0:
        text(d, (W / 2, 1090), "詳しくはショップで", 54, ANKO, bold=False, alpha=a3, base=base)


def scene_cta(base, d, t):
    a = ease_back(t / 0.45)
    pill(base, W / 2, 600, 840 * min(1, max(a, 0)), 180, ANKO)
    if a > 0.6:
        text(d, (W / 2, 600), "数量限定", 80, WHITE)
    a2 = ease_out((t - 0.5) / 0.4)
    if a2 > 0:
        text(d, (W / 2, 800), "TOKKIのBASEショップで", 58, ANKO, alpha=a2, base=base)
        text(d, (W / 2, 890), "販売中", 58, ANKO, alpha=a2, base=base)
    a3 = ease_back((t - 1.0) / 0.45)
    if a3 > 0:
        pulse = 1 + 0.03 * math.sin(t * 6)
        pill(base, W / 2, 1110, 900 * min(1, max(a3, 0)) * pulse, 200, PINK)
        if a3 > 0.6:
            text(d, (W / 2, 1080), "プロフィールのリンク", 58, WHITE)
            text(d, (W / 2, 1150), "からどうぞ", 58, WHITE)
    a4 = ease_out((t - 1.6) / 0.4)
    if a4 > 0:
        text(d, (W / 2, 1330), "「口金」とコメントでURLもお送りします", 42, ANKO, bold=False,
             alpha=a4, base=base)


SCENES = [
    (2.8, scene_hook),
    (3.6, scene_set),
    (3.0, scene_ship),
    (3.4, scene_cta),
]

if __name__ == "__main__":
    render(SCENES, OUT)
