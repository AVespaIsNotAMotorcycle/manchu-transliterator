from PIL import Image, ImageDraw, ImageFont
import json
import random
import statistics

from utils import pixel_string_to_array

width = 50
height = 350

def colors(code):
    if code == 1: return (0, 0, 0)
    if code == 2: return (255, 0, 0)
    return (255, 255, 255)

def load_image(line_index):
    file = open("training_data.json", "r")
    lines = file.readlines()
    line = lines[line_index]

    line_json = json.loads(line)

    image_string = line_json["image"]
    return pixel_string_to_array(image_string)

def mark_center_line(image_array, color_code = 2):
    L_BUFFER = 1
    R_BUFFER = 0
    starts = []
    ends = []

    V_BUFFER = 10
    v_start = -1
    v_end = -1

    for row_index in range(height):
        start = -1
        end = -1
        for col_index in range(width):
            y = row_index * width
            x = col_index
            pixel = image_array[x + y]

            if pixel == 0: continue

            if start == -1:
                start = x
                end = x
            else:
                end = x

        starts.append(start)
        ends.append(end)

        if v_start == -1 and start != -1:
            v_start = row_index
            v_end = row_index
        if v_start != -1 and start != -1:
            v_end = row_index

    starts = list(filter(lambda x: x >= 0, starts))
    ends = list(filter(lambda x: x >= 0, ends))
    
    if len(starts) == 0: return image_array
    if len(ends) == 0: return image_array

    median_start = statistics.median(starts)
    median_end = statistics.median(ends)

    marked = image_array
    for row_index in range(height):
        for col_index in range(width):
            y = row_index * width
            x = col_index

            if row_index < v_start + V_BUFFER: continue
            if row_index > v_end - V_BUFFER: continue
            if col_index < median_start + L_BUFFER: continue
            if col_index > median_end - R_BUFFER: continue
            image_array[x + y] = color_code
    return marked

def remove_center_line(image_array):
    return mark_center_line(image_array, 0)

def render(image_array):
    image = Image.new(mode = "RGB", size = (width, height), color = (255, 255, 255))
    draw = ImageDraw.Draw(image)

    for index in range(len(image_array)):
        pixel = image_array[index]
        if pixel == 0: continue

        x = index % width
        y = int((index - x) / width)
        draw.point([x,y], fill = colors(pixel))
    image.show()

def preprocess(image_array, show = False):
    if show: render(image_array)
    if show: render(mark_center_line(image_array))
    if show: render(remove_center_line(image_array))
    return remove_center_line(image_array)

'''
NUM_ENTRIES = 51358
image_array = load_image(random.randrange(NUM_ENTRIES))
preprocess(image_array)
'''
