import numpy as np
import math
import json
import unicodedata

from abkai import manchu_to_abkai
from utils import INPUT_LAYER_SIZE, pixel_string_to_array
from preprocessing import preprocess

ALPHABET = [
    " ", # EMPTY
    "ᠸ", # MONGGOLIAN LETTER WA
    "ᡝ", # MONGGOLIAN LETTER SIBE E
    "ᡳ", # MONGGOLIAN LETTER MANCHU I
    "ᠯ", # MONGGOLIAN LETTER LA
    "ᠪ", # MONGGOLIAN LETTER BA
    "ᡩ", # MONGGOLIAN LETTER SIBE DA
    "ᡵ", # MONGGOLIAN LETTER MANCHU RA
    "ᠵ", # MONGGOLIAN LETTER JA
    "ᠠ", # MONGGOLIAN LETTER A
    "ᠩ", # MONGGOLIAN LETTER ANG
    "ᡤ", # MONGGOLIAN LETTER SIBE GA
    "ᠨ", # MONGGOLIAN LETTER NA
    "ᡴ", # MONGGOLIAN LETTER MANCHU KA
    "ᠴ", # MONGGOLIAN LETTER CHA
    "ᡠ", # MONGGOLIAN LETTER SIBE UE
    "ᡥ", # MONGGOLIAN LETTER SIBE HA
    "ᡡ", # MONGGOLIAN LETTER SIBE U
    "ᠮ", # MONGGOLIAN LETTER MA
    "ᠣ", # MONGGOLIAN LETTER O
    "ᡧ", # MONGGOLIAN LETTER SIBE SHA
    "ᡶ", # MONGGOLIAN LETTER MANCHU FA
    "ᠶ", # MONGGOLIAN LETTER YA
    "ᠰ", # MONGGOLIAN LETTER SA
    "ᡬ", # MONGGOLIAN LETTER SIBE GAA
    "ᡨ", # MONGGOLIAN LETTER SIBE TA
    "ᡰ", # MONGGOLIAN LETTER SIBE RAA
    "ᡦ", # MONGGOLIAN LETTER SIBE PA
    "᠈", # MONGGOLIAN MANCHU COMMA
    "᠉", # MONGGOLIAN MANCHU FULL STOP
    "ᠺ", # MONGGOLIAN LETTER KA
    "ᡮ", # MONGGOLIAN LETTER SIBE TSA
    "ᡟ", # MONGGOLIAN LETTER SIBE IY
    "ᡯ", # MONGGOLIAN LETTER SIBE ZA
    "ᡱ", # MONGGOLIAN LETTER SIBE CHA
    "ᡭ", # MONGGOLIAN LETTER SIBE HAA
    "", # MONGGOLIAN VOWEL SEPARATOR
    "ᡷ", # MONGGOLIAN LETTER MANCHU ZHA
    "\u180b", # MONGOLIAN FREE VARIATION SELECTOR ONE
]

INPUT_LAYER_SIZE = 50 * 350
WORD_MAX_CHARACTERS = 30
CHARACTERS_IN_ALPHABET = len(ALPHABET)
OUTPUT_LAYER_SIZE = WORD_MAX_CHARACTERS * CHARACTERS_IN_ALPHABET

class NeuralNetwork:
    LEARNING_RATE = 0.1
    _use_file = True
    NN_FILE_PATH = "saved_ann.json"

    def _rand_initialize_weights(self, size_in, size_out):
        return [((x * 0.12) - 0.06) for x in np.random.rand(size_out, size_in)]
    
    def _sigmoid_scalar(self, z):
        if z >= 15: return 1
        if z <= -15: return 0
        return 1 / (1 + math.e ** -z)
    
    def __init__(self, num_hidden_nodes):
        print("Initializing neural network")
        self.theta1 = self._rand_initialize_weights(INPUT_LAYER_SIZE, num_hidden_nodes)
        self.theta2 = self._rand_initialize_weights(num_hidden_nodes, OUTPUT_LAYER_SIZE)
        self.input_layer_bias = self._rand_initialize_weights(1, num_hidden_nodes)
        self.hidden_layer_bias = self._rand_initialize_weights(1, OUTPUT_LAYER_SIZE)
   
    def word_to_array(self, input_word):
        word = input_word.strip().ljust(WORD_MAX_CHARACTERS, ' ')
        array = [0] * OUTPUT_LAYER_SIZE
        for i in range(len(word)):
            char = word[i]
            if char not in ALPHABET: print("[{0}] {1}".format(char, unicodedata.name(char)))
            char_index = ALPHABET.index(char)
            array_index = (i * CHARACTERS_IN_ALPHABET) + char_index
            array[array_index] = 1
        return array

    def array_to_word(self, array):
        word = ""
        for char_index in range(WORD_MAX_CHARACTERS):
            start_index = char_index * CHARACTERS_IN_ALPHABET
            end_index = start_index + CHARACTERS_IN_ALPHABET

            max_certainty = 0
            max_index = start_index
            for i in range(start_index, end_index):
                certainty = array[i]
                if certainty > max_certainty:
                    max_certainty = certainty
                    max_index = i
            letter_index = max_index - start_index
            letter = ALPHABET[letter_index]
            word += letter
        return word.strip()

    def sigmoid(self, matrix):
        sigmoid_to_matrix = np.vectorize(self._sigmoid_scalar)
        new_matrix = sigmoid_to_matrix(matrix)
        return new_matrix

    def forward_propogate(self, pixels):
        y1 = np.dot(np.asmatrix(self.theta1), np.asmatrix(pixels).T)
        y1 = y1 + np.asmatrix(self.input_layer_bias)
        y1 = self.sigmoid(y1)
    
        y2 = np.dot(np.array(self.theta2), y1)
        y2 = y2 + np.asmatrix(self.hidden_layer_bias)
        y2 = self.sigmoid(y2)

        predictions = y2.T.tolist()[0]

        results = {
            "y1": y1,
            "y2": y2,
            "predictions": predictions,
        }
        return results

    def print_word_array(self, word):
        array = self.word_to_array(word)
        line = ""
        char = '_'
        sumline = 0
        print(word)
        for index in range(len(array)):
            if index > 0: line += ' '
            if index % CHARACTERS_IN_ALPHABET == 0 and index > 0:
                print("'{0}' | {1} | {2}\n".format(char, line, sumline))
                line = ""
                char = '_'
                sumline = 0
            line += str(array[index])
            if array[index] == 1:
                char = ALPHABET[index % CHARACTERS_IN_ALPHABET]
                sumline += 1

    def back_propogate(self, pixels, results, actual_word):
        y1 = results['y1']
        y2 = results['y2']

        # self.print_word_array(actual_word)
        actual_vals = self.word_to_array(actual_word)
        output_errors = np.asmatrix(actual_vals).T - np.asmatrix(y2)
        hidden_errors = np.multiply(np.dot(np.asmatrix(self.theta2).T, output_errors), y1)
    
        self.theta1 += self.LEARNING_RATE * np.dot(np.asmatrix(hidden_errors), np.asmatrix(pixels))
        self.theta2 += self.LEARNING_RATE * np.dot(np.asmatrix(output_errors), np.asmatrix(y1).T)
        self.hidden_layer_bias += self.LEARNING_RATE * output_errors
        self.input_layer_bias += self.LEARNING_RATE * hidden_errors

    def save(self):
        if not self._use_file:
            return

        json_neural_network = {
            "theta1":[np_mat.tolist()[0] for np_mat in self.theta1],
            "theta2":[np_mat.tolist()[0] for np_mat in self.theta2],
            "b1":self.input_layer_bias[0].tolist()[0],
            "b2":self.hidden_layer_bias[0].tolist()[0]
        };
        with open(self.NN_FILE_PATH,'w') as nnFile:
            json.dump(json_neural_network, nnFile)

    def _load(self):
        if not self._use_file:
            return

        with open(self.NN_FILE_PATH) as nnFile:
            nn = json.load(nnFile)
        self.theta1 = [np.array(li) for li in nn['theta1']]
        self.theta2 = [np.array(li) for li in nn['theta2']]
        self.input_layer_bias = [np.array(nn['b1'][0])]
        self.hidden_layer_bias = [np.array(nn['b2'][0])]
    
    def predict(self, test):
        pixel_string = test["image"]
        pixels = pixel_string_to_array(pixel_string)
        pixels = preprocess(pixels)
        predictions = self.forward_propogate(pixels)['predictions']
   
        '''
        # HOLDOVER FROM OCR TUTORIAL
        highest_confidence = max(predictions)
        confidence_percent = int(highest_confidence * 100)
        prediction = predictions.index(highest_confidence)
        print("Predicting digit is {0} with {1}% confidence".format(prediction, confidence_percent))
        return { "digit": predictions.index(max(predictions)), "confidence": confidence_percent }
        '''
        word = self.array_to_word(predictions)
        return { "array": predictions, "word": word }

    def train_on_example(self, pixel_string, actual_word):
        pixels = pixel_string_to_array(pixel_string)
        pixels = preprocess(pixels)
        output = self.forward_propogate(pixels)

        
        pred_array = output["predictions"]
        pred_word = self.array_to_word(pred_array)

        self.back_propogate(pixels, output, actual_word)
        return { "prediction": pred_word, "actual": actual_word }

    def word_similarity(self, a, b):
        padded_a = a.ljust(WORD_MAX_CHARACTERS, " ")
        padded_b = b.ljust(WORD_MAX_CHARACTERS, " ")

        matches = 0
        for index in range(len(padded_a)):
            char_a = padded_a[index]
            char_b = padded_b[index]
            if char_a == char_b: matches += 1

        return int(matches / WORD_MAX_CHARACTERS * 100)

    def train(self, training_data):
        predictions = []
        # for example in training_data:
        for index in range(len(training_data)):
            example = training_data[index]
            prediction = self.train_on_example(example['image'], example['word'])
            print("{0} | {1}% | {2} | {3}".format(str(index).rjust(6, ' '),
                                                 str(self.word_similarity(prediction['prediction'],
                                                                          prediction['actual']))
                                                  .rjust(3, " "),
                                                 manchu_to_abkai(prediction['prediction']).ljust(WORD_MAX_CHARACTERS, " "),
                                                 manchu_to_abkai(prediction['actual'])))
            predictions.append(prediction)
        return predictions
