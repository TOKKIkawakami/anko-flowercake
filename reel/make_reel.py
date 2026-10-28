"""あんフラワーケーキ道具紹介リール（1080x1920 / 30fps）を生成する。

使い方: python3 reel/make_reel.py  → reel/tokki_tools_reel.mp4
"""
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT = ROOT / "reel" / "tokki_tools_reel.mp4"

W, H, FPS = 1080, 1920, 30
# Noto Sans JP（可変ウェイト・OFL）。本物の太字を使い、画数の多い字がつぶれないようにする
FONT = ASSETS / "fonts" / "NotoSansJP.ttf"

# あんこ×桜ピンクの配色
BG = (253, 244, 240)
PINK = (232, 106, 133)
PINK_LIGHT = (250, 222, 228)
ANKO = (92, 52, 44)
WHITE = (255, 255, 255)

_font_cache = {}


def font(size, weight=500):
    key = (size, weight)
    if key not in _font_cache:
        f = ImageFont.truetype(str(FONT), size)
        f.set_variation_by_axes([weight])
        _font_cache[key] = f
    return _font_cache[key]


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_back(t):
    t = max(0.0, min(1.0, t))
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def text(draw, xy, s, size, fill, anchor="mm", bold=True, alpha=1.0, base=None):
    """alpha<1のときは別レイヤーに描いて合成する。"""
    f = font(size, 800 if bold else 500)
    if alpha >= 0.999:
        draw.text(xy, s, font=f, fill=fill, anchor=anchor)
        return
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text(xy, s, font=f, fill=fill + (255,), anchor=anchor)
    a = layer.getchannel("A").point(lambda v: int(v * alpha))
    layer.putalpha(a)
    base.alpha_composite(layer)


def pill(base, cx, cy, w, h, color, alpha=1.0):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(
        (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=h / 2,
        fill=color + (int(255 * alpha),))
    base.alpha_composite(layer)


def card(img_path, size, radius=48):
    """白背景の商品写真を角丸カード＋影にする。"""
    im = Image.open(img_path).convert("RGB")
    cw, ch = size
    scale = max(cw / im.width, ch / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    left, top = (im.width - cw) // 2, (im.height - ch) // 2
    im = im.crop((left, top, left + cw, top + ch))
    mask = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw, ch), radius=radius, fill=255)
    pad = 60
    out = Image.new("RGBA", (cw + pad * 2, ch + pad * 2), (0, 0, 0, 0))
    shadow = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (pad, pad + 16, pad + cw, pad + ch + 16), radius=radius, fill=(120, 60, 60, 70))
    out.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(22)))
    im = im.convert("RGBA")
    im.putalpha(mask)
    out.alpha_composite(im, (pad, pad))
    return out


def paste(base, im, cx, cy, scale=1.0, alpha=1.0):
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))),
                       Image.BILINEAR)
    if alpha < 0.999:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def background(t):
    """ゆっくり漂う花びら風の丸。"""
    base = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(base)
    for i in range(14):
        x = (i * 173 + t * (18 + i * 3)) % (W + 200) - 100
        y = (i * 311 + t * (30 + i * 5)) % (H + 200) - 100
        r = 26 + (i * 13) % 40
        d.ellipse((x - r, y - r * 0.7, x + r, y + r * 0.7), fill=PINK_LIGHT + (255,))
    return base


def brand(base, d, label="あんフラワーケーキの道具"):
    # 上部ブランド表記（IGのUIを避けて少し下げる）
    d.text((W / 2, 170), f"TOKKI  |  {label}", font=font(34),
           fill=ANKO, anchor="mm")


# ---- シーン定義 --------------------------------------------------------------

CARD103 = card(ASSETS / "wilton103.png", (900, 600))
CARD104 = card(ASSETS / "wilton104.png", (900, 600))
CARDLIFT = card(ASSETS / "flower_lifter.png", (640, 640))


def scene_hook(base, d, t):
    a1 = ease_out(t / 0.5)
    text(d, (W / 2, 640 - 40 * (1 - a1)), "あんフラワーケーキ", 92, ANKO, alpha=a1, base=base)
    text(d, (W / 2, 770 - 40 * (1 - a1)), "作ってる人へ", 92, ANKO, alpha=a1, base=base)
    a2 = ease_back((t - 0.7) / 0.5)
    if a2 > 0:
        pill(base, W / 2, 1010, 860 * min(1, a2), 170, PINK)
        if a2 > 0.6:
            text(d, (W / 2, 1010), "この道具、探してない？", 74, WHITE)
    a3 = ease_out((t - 1.6) / 0.5)
    if a3 > 0:
        text(d, (W / 2, 1210), "品薄で見つからない3つ、まとめました", 46, ANKO, bold=False,
             alpha=a3, base=base)


def tool_scene(card_img, num, name, lines):
    def scene(base, d, t):
        brand(base, d)
        a = ease_out(t / 0.45)
        pill(base, 200, 330, 200, 90, PINK, alpha=a)
        text(d, (200, 330), num, 52, WHITE, alpha=a, base=base)
        text(d, (W / 2 + 60 * (1 - a), 470), name, 88, ANKO, alpha=a, base=base)
        s = ease_back((t - 0.2) / 0.6)
        if s > 0:
            paste(base, card_img, W / 2, 900, scale=0.6 + 0.4 * s, alpha=min(1, s))
        for i, ln in enumerate(lines):
            la = ease_out((t - 0.9 - i * 0.35) / 0.4)
            if la > 0:
                y = 1330 + i * 105
                text(d, (W / 2, y + 30 * (1 - la)), ln, 54 if i == 0 else 46,
                     PINK if i == 0 else ANKO, bold=(i == 0), alpha=la, base=base)
    return scene


def scene_soldout(base, d, t):
    shake = math.sin(t * 40) * 10 * max(0, 1 - t / 0.5)
    a = ease_back(t / 0.5)
    pill(base, W / 2 + shake, 760, 760 * min(1, max(a, 0)), 200, ANKO)
    if a > 0.6:
        text(d, (W / 2 + shake, 760), "どれも今 品薄…！", 84, WHITE)
    a2 = ease_out((t - 0.8) / 0.5)
    if a2 > 0:
        text(d, (W / 2, 990), "ネットでも売り切れが続いていて", 50, ANKO, bold=False, alpha=a2, base=base)
        text(d, (W / 2, 1075), "探している人が多いんです", 50, ANKO, bold=False, alpha=a2, base=base)
    # 3点を小さく並べる
    a3 = ease_out((t - 1.4) / 0.5)
    if a3 > 0:
        for i, c in enumerate((CARD103, CARD104, CARDLIFT)):
            paste(base, c, 220 + i * 320, 1330 + 30 * (1 - a3), scale=0.3 if i < 2 else 0.4, alpha=a3)


def scene_cta(base, d, t):
    a = ease_back(t / 0.5)
    pill(base, W / 2, 560, 820 * min(1, max(a, 0)), 190, PINK)
    if a > 0.6:
        text(d, (W / 2, 560), "TOKKIで取り扱い中", 78, WHITE)
    a2 = ease_out((t - 0.6) / 0.5)
    if a2 > 0:
        for i, ln in enumerate(["Wilton #103", "Wilton #104", "フラワーリフター"]):
            text(d, (W / 2, 760 + i * 90), ln, 56, ANKO, alpha=a2, base=base)
    a3 = ease_out((t - 1.3) / 0.5)
    if a3 > 0:
        text(d, (W / 2, 1110), "探してる友だちに", 64, ANKO, alpha=a3, base=base)
        text(d, (W / 2, 1200), "教えてあげてね", 64, ANKO, alpha=a3, base=base)
    a4 = ease_back((t - 2.0) / 0.5)
    if a4 > 0:
        pulse = 1 + 0.03 * math.sin(t * 6)
        pill(base, W / 2, 1390, 760 * min(1, max(a4, 0)) * pulse, 130, ANKO)
        if a4 > 0.6:
            text(d, (W / 2, 1390), "ご注文・在庫はDMへ", 56, WHITE)
    a5 = ease_out((t - 2.6) / 0.5)
    if a5 > 0:
        text(d, (W / 2, 1520), "保存＆シェアで見返せます", 42, PINK, bold=False, alpha=a5, base=base)


SCENES = [
    (3.2, scene_hook),
    (4.6, tool_scene(CARD103, "No.1", "Wilton #103",
                     ["小さめの花びら口金", "バラの中心・小花・つぼみに"])),
    (4.6, tool_scene(CARD104, "No.2", "Wilton #104",
                     ["定番サイズの花びら口金", "バラの外側・カーネーションに"])),
    (4.6, tool_scene(CARDLIFT, "No.3", "フラワーリフター",
                     ["絞った花をはさんで移動", "形を崩さずケーキに配置できる"])),
    (3.4, scene_soldout),
    (4.6, scene_cta),
]

FADE = 0.25  # シーン切り替えのフェード秒数


def render(scenes=None, out=None, bg_fn=None, fade_color=None):
    bg_fn = bg_fn or background
    fade_color = fade_color or BG
    scenes = scenes or SCENES
    out = out or OUT
    total = sum(s[0] for s in scenes)
    n = int(total * FPS)
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
         "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", str(out)],
        stdin=subprocess.PIPE)
    for f in range(n):
        g = f / FPS
        start = 0.0
        for dur, fn in scenes:
            if g < start + dur:
                break
            start += dur
        t = g - start
        base = bg_fn(g)
        d = ImageDraw.Draw(base)
        fn(base, d, t)
        # 前後フェード（白へ）
        fade = 0.0
        if t > dur - FADE and fn is not scenes[-1][1]:
            fade = (t - (dur - FADE)) / FADE
        elif t < FADE and start > 0:
            fade = 1 - t / FADE
        if fade > 0:
            base = Image.blend(base, Image.new("RGBA", (W, H), fade_color + (255,)), min(1, fade) * 0.9)
        ff.stdin.write(base.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    print(f"wrote {out} ({total:.1f}s, {n} frames)")


if __name__ == "__main__":
    render()
