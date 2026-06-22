from PIL import Image, ImageDraw, ImageFont
import json

width = 50
height = 350

def load_image(line_index):
    file = open("../training_data.json", "r")
    lines = file.readlines()
    line = lines[line_index]

    line_json = json.loads(line)
    print(line_json)

    image = Image.new(mode = "RGB", size = (width, height), color = (255, 255, 255))
    draw = ImageDraw.Draw(image)

    image_string = line_json["image"]
    for index in range(len(image_string)):
        char = image_string[index]
        if char == '0': continue

        x = index % width
        y = int((index - x) / width)
        draw.point([x,y], fill = (0, 0, 0))
    image.show()

load_image(0)
load_image(7)
load_image(23)
load_image(54)
load_image(55)
load_image(60)
load_image(71)
