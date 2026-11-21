"""道具の補充＋チュンソル1kg 販売誘導リール 1080x1920 / 約19秒。

使い方: python3 reel/make_tools_restock_reel.py → reel/tokki_tools_restock_reel.mp4
道具はピンク背景、最後のあんこはベージュ水玉背景（「ピンク＝道具、ベージュ＝あんこ」で統一）。
"""
import math

from make_practice_reel import background_anko
from make_reel import (ANKO, ASSETS, PINK, ROOT, W, WHITE, background, brand,
                       card, ease_back, ease_out, paste, pill, render, text)

OUT = ROOT / "reel" / "tokki_tools_restock_reel.mp4"
LABEL = "あんフラワーの道具"
OCHRE = (196, 122, 32)  # あんこ側のアクセント色

TOOLS = [
    (card(ASSETS / "wilton123.png", (900, 600), fit=True), "Wilton #123",
     "大きな花びら口金", "大輪のバラ・ピオニーに"),
    (card(ASSETS / "flower_nail.png", (640, 640), fit=True), "フラワーネイル",
     "花を絞る台", "回しながら花びらを重ねる"),
    (card(ASSETS / "flower_sheet_5cm.png", (640, 640), fit=True), "フラワーシート 5cm",
     "ネイルの上に敷くシート", "絞った花をそのまま移せる"),
    (card(ASSETS / "piping_bag.png", (640, 640), fit=True), "絞り袋",
     "口金をセットして使う", "あんこを詰めて絞るだけ"),
    (card(ASSETS / "scraper.png", (640, 640), fit=True), "スクレーパー",
     "あんこを練る・まとめる", "色づけや下準備に"),
]
CARD_ANKO = card(ASSETS / "chunseol_logo.png", (460, 530), radius=40)


def scene_hook(base, d, t):
    a1 = ease_out(t / 0.4)
    text(d, (W / 2, 680 - 40 * (1 - a1)), "あんフラワーの道具", 92, ANKO, alpha=a1, base=base)
    text(d, (W / 2, 810 - 40 * (1 - a1)), "補充しました！", 92, ANKO, alpha=a1, base=base)
    a2 = ease_back((t - 0.7) / 0.45)
    if a2 > 0:
        pill(base, W / 2, 1050, 820 * min(1, a2), 180, PINK)
        if a2 > 0.6:
            text(d, (W / 2, 1050), "新しい道具も追加", 76, WHITE)
    a3 = ease_out((t - 1.3) / 0.4)
    if a3 > 0:
        text(d, (W / 2, 1230), "TOKKIで買えます", 54, ANKO, alpha=a3, base=base)


def tool_scene(i, card_img, name, line1, line2):
    def scene(base, d, t):
        brand(base, d, LABEL)
        a = ease_out(t / 0.35)
        pill(base, W / 2, 330, 190, 80, PINK, alpha=a)
        text(d, (W / 2, 330), f"{i + 1} / {len(TOOLS)}", 44, WHITE, alpha=a, base=base)
        text(d, (W / 2 + 50 * (1 - a), 460), name, 84, ANKO, alpha=a, base=base)
        s = ease_back((t - 0.1) / 0.5)
        if s > 0:
            scale = 0.85 if card_img.width > 900 else 0.95
            paste(base, card_img, W / 2, 870, scale=scale * (0.7 + 0.3 * s), alpha=min(1, s))
        a2 = ease_out((t - 0.5) / 0.35)
        if a2 > 0:
            text(d, (W / 2, 1290 + 30 * (1 - a2)), line1, 56, PINK, alpha=a2, base=base)
            text(d, (W / 2, 1390 + 30 * (1 - a2)), line2, 46, ANKO, bold=False, alpha=a2, base=base)
    return scene


def scene_anko(base, d, t):
    brand(base, d, "あんこも入荷しました")
    a = ease_out(t / 0.4)
    text(d, (W / 2, 400), "最後にあんこも！", 84, ANKO, alpha=a, base=base)
    s = ease_back((t - 0.2) / 0.5)
    if s > 0:
        paste(base, CARD_ANKO, W / 2, 820, scale=0.7 + 0.3 * s, alpha=min(1, s))
    a2 = ease_out((t - 0.7) / 0.4)
    if a2 > 0:
        text(d, (W / 2, 1180), "チュンソル 白あん 1kg", 62, ANKO, alpha=a2, base=base)
        text(d, (W / 2, 1290), "1,080円（税込）", 80, OCHRE, alpha=a2, base=base)
    a3 = ease_out((t - 1.2) / 0.4)
    if a3 > 0:
        text(d, (W / 2, 1420), "まずは試してみたい方にちょうどいい量", 44, ANKO, bold=False,
             alpha=a3, base=base)


def scene_cta(base, d, t):
    a = ease_back(t / 0.45)
    pill(base, W / 2, 560, 860 * min(1, max(a, 0)), 170, ANKO)
    if a > 0.6:
        text(d, (W / 2, 560), "あんこ＋道具で", 66, WHITE)
    a1 = ease_out((t - 0.3) / 0.4)
    if a1 > 0:
        text(d, (W / 2, 720), "送料は1回分", 80, PINK, alpha=a1, base=base)
    a2 = ease_out((t - 0.7) / 0.4)
    if a2 > 0:
        text(d, (W / 2, 880), "数量限定・TOKKIのBASEショップで", 50, ANKO, alpha=a2, base=base)
    a3 = ease_back((t - 1.1) / 0.45)
    if a3 > 0:
        pulse = 1 + 0.03 * math.sin(t * 6)
        pill(base, W / 2, 1090, 900 * min(1, max(a3, 0)) * pulse, 200, PINK)
        if a3 > 0.6:
            text(d, (W / 2, 1060), "プロフィールのリンク", 58, WHITE)
            text(d, (W / 2, 1130), "からどうぞ", 58, WHITE)
    a4 = ease_out((t - 1.7) / 0.4)
    if a4 > 0:
        text(d, (W / 2, 1310), "「道具」とコメントでURLもお送りします", 42, ANKO, bold=False,
             alpha=a4, base=base)


SCENES = [(2.6, scene_hook)]
SCENES += [(2.0, tool_scene(i, *tool)) for i, tool in enumerate(TOOLS)]
SCENES += [(3.2, scene_anko), (3.6, scene_cta)]

# あんこのシーンだけベージュ背景にする
_ANKO_START = sum(dur for dur, _ in SCENES[:-2])
_ANKO_END = _ANKO_START + SCENES[-2][0]


def bg(g):
    return background_anko(g) if _ANKO_START <= g < _ANKO_END else background(g)


if __name__ == "__main__":
    render(SCENES, OUT, bg_fn=bg)
