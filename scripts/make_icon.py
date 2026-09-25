#!/usr/bin/env python3
"""生成 512x512 图标：深色圆角方块 + 一个平滑的对话气泡曲线。"""
from PIL import Image, ImageDraw
S = 512
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
# 背景：圆角方形，垂直渐变
bg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
bd = ImageDraw.Draw(bg)
top, bot = (28, 30, 38), (14, 15, 20)
for y in range(S):
    t = y / (S - 1)
    c = tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)) + (255,)
    bd.line([(0, y), (S, y)], fill=c)
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=112, fill=255)
img.paste(bg, (0, 0), mask)
# 气泡：柔和的浅色
d = ImageDraw.Draw(img)
bubble = (245, 240, 230, 255)
d.rounded_rectangle([96, 136, 416, 340], radius=72, fill=bubble)
d.polygon([(168, 330), (150, 402), (232, 338)], fill=bubble)
# 气泡内的一条平滑波浪线，代表"顺滑"
import math
pts = []
for i in range(0, 201):
    x = 150 + i * (212 / 200)
    y = 238 + 26 * math.sin(i / 200 * math.pi * 2)
    pts.append((x, y))
d.line(pts, fill=(20, 22, 30, 255), width=22, joint="curve")
img.save("assets/icon-512.png")
img.resize((128, 128), Image.LANCZOS).save("assets/icon-128.png")
print("icon written")
