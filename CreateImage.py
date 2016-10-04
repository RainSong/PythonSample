# -*- coding:utf-8 -*-

from PIL import Image, ImageFile, ImageDraw,ImageFont

image = Image.open('e:\\TranscodedWallpaper.jpg')
image = image.convert('RGBA')

text = Image.new('RGBA', image.size, (255, 255, 255, 0))

font = ImageFont.truetype('D:\\Windows\\Fonts\\微软雅黑\\msyh.ttf',size=40)

draw = ImageDraw.Draw(text)

draw.text((800,100),'Hello',font=font,fill=(255,255,255,128))
draw.text((800,160),'World',font=font,fill=(255,255,255,255))

out = Image.alpha_composite(image,text)

# draw = ImageDraw.Draw(image)
out.show()
