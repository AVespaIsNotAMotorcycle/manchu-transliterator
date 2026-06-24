from PIL import Image, ImageDraw, ImageFont
import json
import random
import statistics

from utils import pixel_string_to_array

WIDTH = 50
HEIGHT = 350

COMPRESSED_WIDTH = 8
JOINT_COMPRESSED_WIDTH = COMPRESSED_WIDTH * 2 + 1

def colors(code):
    if code == 1: return (0, 0, 0)
    if code == 2: return (255, 0, 0)
    if code == 3: return (0, 255, 0)
    if code == 4: return (0, 0, 255)
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

    for row_index in range(HEIGHT):
        start = -1
        end = -1
        for col_index in range(WIDTH):
            y = row_index * WIDTH
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

    marked = image_array.copy()
    for row_index in range(HEIGHT):
        for col_index in range(WIDTH):
            y = row_index * WIDTH
            x = col_index

            if row_index < v_start + V_BUFFER: continue
            if row_index > v_end - V_BUFFER: continue
            if col_index < median_start + L_BUFFER: continue
            if col_index > median_end - R_BUFFER: continue
            marked[x + y] = color_code
    return marked

def remove_center_line(image_array):
    return mark_center_line(image_array, 0)

def render(image_array, width = WIDTH):
    image = Image.new(mode = "RGB", size = (width, HEIGHT), color = (255, 255, 255))
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

def start_of_color_block(image_array, color_code):
    start = -1
    end = -1
    
    for row_index in range(HEIGHT):
        for col_index in range(WIDTH):
            y = row_index * WIDTH
            x = col_index
            pixel = image_array[x + y]

            if pixel != color_code:
                if end > start: return [start, end]
                else: continue

            if start == -1: start = x
            if x > end: end = x
    return [start, end]

def extrema_black_columns(image_array, width):
    leftmost = width
    rightmost = 0
    for row_index in range(HEIGHT):
        for col_index in range(width):
            y = row_index * width
            x = col_index
            pixel = image_array[x + y]

            if pixel == 1:
                if x < leftmost:
                    leftmost = x
                if x > rightmost:
                    rightmost = x
    return [leftmost, rightmost]

def compress_row(row):
    if len(row) == COMPRESSED_WIDTH:
        return row
    if 1 not in row:
        return [0] * COMPRESSED_WIDTH

    compressed_row = []

    if len(row) > COMPRESSED_WIDTH:
        scale = len(row) / COMPRESSED_WIDTH
        for i in range(COMPRESSED_WIDTH):
            start = int(i * scale)
            end = int((i + 1) * scale)
            chunk = row[start:end]

            if 1 in chunk: compressed_row.append(1)
            else: compressed_row.append(0)
    else:
        for pixel in row:
            compressed_row.append(pixel)
        while len(compressed_row) < COMPRESSED_WIDTH:
            compressed_row.append(0)

    return compressed_row

def compress_half(image_array, width):
    extrema = extrema_black_columns(image_array, width)
    compressed = []
    left = extrema[0]
    right = extrema[1] + 1

    for row_index in range(HEIGHT):
        row = []
        for col_index in range(width):
            y = row_index * width
            x = col_index
            pixel = image_array[x + y]
            row.append(pixel)
        compressed_row = compress_row(row[left:right])
        for pixel in compressed_row:
            compressed.append(pixel)

    return compressed

def join_compressed_halves(left, right):
    joint = []
    for y in range(HEIGHT):
        start = y * COMPRESSED_WIDTH
        end = start + COMPRESSED_WIDTH
        for pixel in left[start:end]: joint.append(pixel)
        joint.append(0)
        for pixel in right[start:end]: joint.append(pixel)
    return joint

def split_halves(image_array, boundaries):
    marked = image_array.copy()

    left_half = []
    left_width = boundaries[1] - boundaries[0]

    right_half = []
    right_width = boundaries[3] - boundaries[2] - 1

    for row_index in range(HEIGHT):
        for col_index in range(WIDTH):
            y = row_index * WIDTH
            x = col_index
            pixel = image_array[x + y]

            if x >= boundaries[0] and x < boundaries[1]:
                left_half.append(pixel)
                if pixel == 0:
                    marked[x + y] = (3)
                    continue
            if x > boundaries[2] and x < boundaries[3]:
                right_half.append(pixel)
                if pixel == 0:
                    marked[x + y] = (4)
                    continue

    compressed_left = compress_half(left_half, left_width)
    compressed_right = compress_half(right_half, right_width)
    joint = join_compressed_halves(compressed_left, compressed_right)
    return joint

def compress(image_array, remove_center_line = True):
    marked_center = mark_center_line(image_array)
    center_line_boundaries = start_of_color_block(marked_center, 2)

    boundaries = [0,
                  center_line_boundaries[0],
                  center_line_boundaries[1],
                  WIDTH]
    compressed = split_halves(image_array, boundaries)
    return compressed

if __name__=="__main__":
    NUM_ENTRIES = 51358
    index = random.randrange(NUM_ENTRIES)
    # index = 36927
    print(index)
    image_array = load_image(index)
    compressed = compress(image_array)
    render(image_array)
    render(compressed, JOINT_COMPRESSED_WIDTH)
