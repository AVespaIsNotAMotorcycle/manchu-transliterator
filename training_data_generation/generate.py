from PIL import Image, ImageDraw, ImageFont

WORD = "ᠰᡳᠨᡩᠠᡥᠠ"

width = 50
height = 500

FONTS = ["XM_BiaoHei.ttf",
         "XM_GuFeng.ttf",
         "XM_LiuYe.ttf",
         "XM_ShuKai.ttf",
         "XM_WenJian.ttf",
         "XM_WenQin.ttf",
         "XM_XingShu.ttf",
         "XM_YaBai.ttf",
         "XM_YingBi.ttf",
         "XM_ZhengBai.ttf",
         "XM_ZhengHei.ttf"]

for font_name in FONTS:
    font = ImageFont.truetype(font_name, 30)

    image = Image.new(mode = "RGB", size = (height, height), color = (255,255,255))
    draw = ImageDraw.Draw(image)
    draw.text((10, height / 2), WORD, fill=(0,0,0), font=font, anchor="lm")

    left = (height - width) / 2
    top = 0
    right = left + width
    bottom = height
    image2= image.rotate(-90).crop([left, top, right, bottom])
    image2.show()
