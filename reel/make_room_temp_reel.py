"""「開封前は常温保管OK」チュンソル白あん 訴求リール 1080x1920 / 約16秒。

使い方: python3 reel/make_room_temp_reel.py → reel/tokki_room_temp_anko_reel.mp4
保管の話は必ず「開封前は」を付ける（袋の表示は開封前の保管方法のため）。
他社商品の名前は出さない。
"""
import math

from make_practice_reel import BG_ANKO, background_anko
from make_reel import (ANKO, ASSETS, ROOT, W, WHITE, brand, card, ease_back,
                       ease_out, paste, pill, render, text)

OUT = ROOT / "reel" / "tokki_room_temp_anko_reel.mp4"
LABEL = "チュンソル 白あん"
OCHRE = (196, 122, 32)
GREEN = (98, 140, 40)  # チェックマーク用（袋の黄緑に合わせた濃いめの緑）
CARD_1KG = card(ASSETS / "chunseol_1kg.png", (620, 620), radius=40, fit=True)


def scene_hook(base, d, t):
    a1 = ease_out(t / 0.4)
    text(d, (W / 2, 660 - 40 * (1 - a1)), "あんフラワーのあんこで", 80, ANKO, alpha=a1, base=base)
    text(d, (W / 2, 780 - 40 * (1 - a1)), "冷蔵庫いっぱいになってない？", 64, ANKO, alpha=a1, base=base)
    a2 = ease_back((t - 0.8) / 0.45)
    if a2 > 0:
        pill(base, W / 2, 1020, 900 * min(1, a2), 190, OCHRE)
        if a2 > 0.6:
            text(d, (W / 2, 1020), "常温で置ける白あん", 80, WHITE)
    a3 = ease_out((t - 1.4) / 0.4)
    if a3 > 0:
        text(d, (W / 2, 1200), "TOKKIにあります", 54, ANKO, alpha=a3, base=base)


def scene_product(base, d, t):
    brand(base, d, LABEL)
    a = ease_out(t / 0.4)
    text(d, (W / 2, 400), "韓国のチュンソル 白あん", 70, ANKO, alpha=a, base=base)
    s = ease_back((t - 0.2) / 0.5)
    if s > 0:
        paste(base, CARD_1KG, W / 2, 820, scale=0.7 + 0.3 * s, alpha=min(1, s))
    a2 = ease_back((t - 0.9) / 0.45)
    if a2 > 0:
        pill(base, W / 2, 1270, 860 * min(1, a2), 170, ANKO)
        if a2 > 0.6:
            text(d, (W / 2, 1270), "開封前は常温保管OK", 72, WHITE)


def scene_merits(base, d, t):
    brand(base, d, LABEL)
    a = ease_out(t / 0.4)
    text(d, (W / 2, 520), "常温だから", 84, ANKO, alpha=a, base=base)
    merits = ["冷蔵庫の場所をとらない", "5kgでもまとめ買いしやすい", "クール便不要で送料お手頃"]
    for i, m in enumerate(merits):
        ai = ease_out((t - 0.5 - i * 0.4) / 0.35)
        if ai <= 0:
            continue
        y = 760 + i * 190
        x = 60 * (1 - ai)
        pill(base, W / 2 + x, y, 900, 140, WHITE, alpha=ai)
        text(d, (190 + x, y), "✓", 64, GREEN, alpha=ai, base=base)
        text(d, (250 + x, y), m, 54, ANKO, anchor="lm", alpha=ai, base=base)


def scene_price(base, d, t):
    brand(base, d, LABEL)
    a = ease_out(t / 0.4)
    text(d, (W / 2, 520), "チュンソル 白あん", 76, ANKO, alpha=a, base=base)
    rows = [("1kg", "1,080円"), ("5kg", "4,860円")]
    for i, (kg, price) in enumerate(rows):
        ai = ease_back((t - 0.3 - i * 0.3) / 0.45)
        if ai <= 0:
            continue
        y = 720 + i * 190
        pill(base, W / 2, y, 760 * min(1, ai), 150, WHITE)
        if ai > 0.6:
            text(d, (330, y), kg, 64, ANKO)
            text(d, (640, y), price, 76, OCHRE)
    a3 = ease_out((t - 1.0) / 0.4)
    if a3 > 0:
        text(d, (W / 2, 1060), "（税込・送料別）", 42, ANKO, bold=False, alpha=a3, base=base)
        text(d, (W / 2, 1150), "※開封後は冷蔵で保管し、早めにお使いください", 36, ANKO,
             bold=False, alpha=a3, base=base)


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
        pill(base, W / 2, 1110, 900 * min(1, max(a3, 0)) * pulse, 200, OCHRE)
        if a3 > 0.6:
            text(d, (W / 2, 1080), "プロフィールのリンク", 58, WHITE)
            text(d, (W / 2, 1150), "からどうぞ", 58, WHITE)
    a4 = ease_out((t - 1.6) / 0.4)
    if a4 > 0:
        text(d, (W / 2, 1330), "「あんこ」とコメントでURLもお送りします", 42, ANKO, bold=False,
             alpha=a4, base=base)


SCENES = [
    (2.8, scene_hook),
    (3.4, scene_product),
    (3.4, scene_merits),
    (3.0, scene_price),
    (3.4, scene_cta),
]

if __name__ == "__main__":
    render(SCENES, OUT, bg_fn=background_anko, fade_color=BG_ANKO)
