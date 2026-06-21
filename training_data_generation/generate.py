from PIL import Image, ImageDraw, ImageFont
import numpy as np
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

def collapse_channels(pixel):
    channel_1 = pixel[0] / 255
    channel_2 = pixel[1] / 255
    channel_3 = pixel[2] / 255

    total_value = channel_1 + channel_2 + channel_3
    average = total_value / 3
    inverse = 1.0 - average

    rounded = np.rint([inverse])[0]
    binary = bool(rounded)
    return binary

def simplify_array(array):
    simplified = []

    for row_index in range(len(array)):
        row = array[row_index]
        new_row = []
        for cell_index in range(len(row)):
            cell = row[cell_index]
            collapsed = collapse_channels(cell)
            new_row.append(collapsed)
        simplified.append(new_row)
    return simplified

def generate_training_data(start_index = 0, end_index = -1):
    entries = read_corpus()

    if end_index == -1: end_index = len(entries)
    if end_index < start_index + 1: end_index = start_index + 1
    if end_index > len(entries): end_index = len(entries)

    training_data = []
    for index in range(start_index, end_index):
        entry = json.loads(entries[index])
        manchu = entry['m'].split(' ')
        for word in manchu:
            images = generate_images(word)
            for image in images:
                image_array = np.array(image)
                simple = simplify_array(image_array)
                training_data.append([simple, word])
    return training_data


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
    image2 = image.rotate(-90).crop([left, top, right, bottom])
    # image2.show()
    return image2

def generate_images(word, font = -1):
    images = []

    if font >= 0 and font < len(FONTS):
        images.append(generate_image(word, font))
        return images

    for i in range(len(FONTS)):
        images.append(generate_image(word, i))
    return images
