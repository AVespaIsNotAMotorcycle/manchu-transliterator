INPUT_LAYER_SIZE = 50 * 350

def pixel_string_to_array(string):
    array = [0] * INPUT_LAYER_SIZE
    for index in range(len(string)):
        char = string[index]
        if char == '1': array[index] = 1
    return array
