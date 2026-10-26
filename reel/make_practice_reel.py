"""練習用あんこ（訳あり特価）告知リール 1080x1920 / 約16秒。

使い方: python3 reel/make_practice_reel.py → reel/tokki_practice_anko_reel.mp4
食用不可の商品なので、食べることを思わせる言葉は入れないこと。
"""
import math

from make_reel import (ANKO, ASSETS, PINK, ROOT, W, WHITE,
                       brand, card, ease_back, ease_out, paste, pill, render, text)

OUT = ROOT / "reel" / "tokki_practice_anko_reel.mp4"
CARD_ANKO = card(ASSETS / "chunseol_5kg.png", (430, 640), radius=40)


def scene_hook(base, d, t):
    a1 = ease_out(t / 0.4)
    text(d, (W / 2, 650 - 40 * (1 - a1)), "あんフラワーの練習", 88, ANKO, alpha=a1, base=base)
    text(d, (W / 2, 770 - 40 * (1 - a1)), "あんこ代、かかりすぎ…", 80, ANKO, alpha=a1, base=base)
    a2 = ease_back((t - 0.6) / 0.45)
    if a2 > 0:
        pill(base, W / 2, 1000, 900 * min(1, a2), 180, PINK)
        if a2 > 0.6:
            text(d, (W / 2, 1000), "練習用あんこ 特価です", 76, WHITE)
    a3 = ease_out((t - 1.3) / 0.4)
    if a3 > 0:
        text(d, (W / 2, 1180), "TOKKI 数量限定", 50, ANKO, alpha=a3, base=base)


def scene_price(base, d, t):
    brand(base, d, "練習用あんこ 特価")
    s = ease_back(t / 0.5)
    if s > 0:
        paste(base, CARD_ANKO, 300, 760, scale=0.6 + 0.4 * s, alpha=min(1, s))
    rows = [("チュンソル", "5kg", "1,100円"), ("ペゴク", "5kg", "1,100円"), ("ペゴク", "1kg", "220円")]
    for i, (name, kg, price) in enumerate(rows):
        a = ease_out((t - 0.4 - i * 0.3) / 0.35)
        if a <= 0:
            continue
        y = 560 + i * 200
        x = 790 + 60 * (1 - a)
        text(d, (x, y - 40), f"{name} {kg}", 46, ANKO, alpha=a, base=base)
        text(d, (x, y + 30), price, 78, PINK, alpha=a, base=base)
    a4 = ease_out((t - 1.5) / 0.4)
    if a4 > 0:
        text(d, (W / 2, 1210), "（税込・送料別）", 40, ANKO, bold=False, alpha=a4, base=base)
        pill(base, W / 2, 1360, 700, 120, ANKO, alpha=a4)
        text(d, (W / 2, 1360), "5kgでも1,100円", 60, WHITE, alpha=a4, base=base)


def scene_why(base, d, t):
    brand(base, d, "練習用あんこ 特価")
    a = ease_out(t / 0.4)
    text(d, (W / 2, 620), "なぜこの価格？", 80, ANKO, alpha=a, base=base)
    a2 = ease_out((t - 0.5) / 0.4)
    if a2 > 0:
        text(d, (W / 2, 800), "賞味期限の関係で", 58, ANKO, bold=False, alpha=a2, base=base)
        text(d, (W / 2, 890), "お届け時には期限が過ぎるため", 52, ANKO, bold=False, alpha=a2, base=base)
    a3 = ease_back((t - 1.1) / 0.45)
    if a3 > 0:
        pill(base, W / 2, 1100, 880 * min(1, a3), 190, PINK)
        if a3 > 0.6:
            text(d, (W / 2, 1100), "練習専用・食用不可", 76, WHITE)
    a4 = ease_out((t - 1.7) / 0.4)
    if a4 > 0:
        text(d, (W / 2, 1290), "失敗を気にせず、絞り放題", 54, ANKO, alpha=a4, base=base)


def scene_cta(base, d, t):
    a = ease_back(t / 0.45)
    pill(base, W / 2, 560, 840 * min(1, max(a, 0)), 180, PINK)
    if a > 0.6:
        text(d, (W / 2, 560), "なくなり次第終了", 76, WHITE)
    a2 = ease_out((t - 0.5) / 0.4)
    if a2 > 0:
        text(d, (W / 2, 760), "TOKKIのBASEショップで", 58, ANKO, alpha=a2, base=base)
        text(d, (W / 2, 850), "販売中", 58, ANKO, alpha=a2, base=base)
    a3 = ease_back((t - 1.0) / 0.45)
    if a3 > 0:
        pulse = 1 + 0.03 * math.sin(t * 6)
        pill(base, W / 2, 1080, 900 * min(1, max(a3, 0)) * pulse, 200, ANKO)
        if a3 > 0.6:
            text(d, (W / 2, 1050), "「練習」とコメントで", 58, WHITE)
            text(d, (W / 2, 1120), "URLをお送りします", 58, WHITE)
    a4 = ease_out((t - 1.6) / 0.4)
    if a4 > 0:
        text(d, (W / 2, 1300), "プロフィールのリンクからも買えます", 42, PINK, bold=False,
             alpha=a4, base=base)


SCENES = [
    (2.6, scene_hook),
    (3.8, scene_price),
    (3.2, scene_why),
    (3.4, scene_cta),
]

if __name__ == "__main__":
    render(SCENES, OUT)
