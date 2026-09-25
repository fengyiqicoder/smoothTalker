#!/usr/bin/env python3
"""512x512 图标：高饱和渐变 + 皎洁的白色微笑弧线。用法: make_icon.py <variant> <out>"""
import sys, math
from PIL import Image, ImageDraw, ImageFilter
K = 4; S = 512 * K
PALETTES = {
    "magenta": ((255, 60, 120), (255, 150, 40)),    # 品红 → 橙
    "violet":  ((110, 40, 255), (0, 210, 255)),     # 电光紫 → 青
    "sun":     ((255, 200, 0), (255, 80, 60)),      # 柠檬黄 → 珊瑚红
    "lime":    ((0, 230, 140), (0, 150, 255)),      # 薄荷绿 → 天蓝
}
def make(variant, out):
    c1, c2 = PALETTES[variant]
    bg = Image.new("RGB", (S, S)); px = bg.load()
    for y in range(S):
        for x in range(0, S, 1):
            t = (x + y) / (2 * S - 2)  # 对角渐变
            px[x, y] = tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=112 * K, fill=255)
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0)); img.paste(bg, (0, 0), mask)
    # 微笑：圆弧，圆心在上方，用圆点堆叠保证平滑
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    cx, cy, R, r = 256 * K, 150 * K, 190 * K, 26 * K
    a0, a1 = math.radians(35), math.radians(145)
    for i in range(0, 1201):
        a = a0 + (a1 - a0) * i / 1200
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 255))
    # 两只眼睛：小圆点
    for ex in (176 * K, 336 * K):
        d.ellipse([ex - 22 * K, 168 * K - 22 * K, ex + 22 * K, 168 * K + 22 * K], fill=(255, 255, 255, 255))
    # 柔光：白色元素的轻微外发光
    glow = layer.filter(ImageFilter.GaussianBlur(10 * K))
    img = Image.alpha_composite(img, Image.blend(Image.new("RGBA", (S, S), (0, 0, 0, 0)), glow, 0.55))
    img = Image.alpha_composite(img, layer)
    img.resize((512, 512), Image.LANCZOS).save(out)
    print("wrote", out)
if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2])
