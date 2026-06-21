from PIL import Image, ImageDraw, ImageFont
import random
import json

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


def read_corpus():
    file = open("db.json", "r", encoding="utf-8")
    entries = file.readlines()
    file.close()
    return entries

def generate_random_image():
    entries = read_corpus()
    index = random.randrange(len(entries))
    entry = json.loads(entries[index])
    abkai = entry['r'].split(' ')
    words = entry['m'].split(' ')
    for word in words:
        generate_images(word, random.randrange(len(FONTS)))
    print(words, abkai)

def generate_image(word, font = 0):
    font_name = FONTS[font]
    font = ImageFont.truetype(font_name, 30)

    image = Image.new(mode = "RGB", size = (height, height), color = (255,255,255))
    draw = ImageDraw.Draw(image)
    draw.text((10, height / 2), word, fill=(0,0,0), font=font, anchor="lm")

    left = (height - width) / 2
    top = 0
    right = left + width
    bottom = height
    image2= image.rotate(-90).crop([left, top, right, bottom])
    image2.show()
    return

def generate_images(word, font = -1):
    if font >= 0 and font < len(FONTS):
        return generate_image(word, font)

    for i in range(len(FONTS)):
        generate_image(word, i)

generate_random_image()
