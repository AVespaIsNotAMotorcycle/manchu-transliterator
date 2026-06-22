import numpy as np
import math
import json

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
    "", # MONGGOLIAN FREE VARIATION SELECTOR ONE
    "᠉", # MONGGOLIAN MANCHU FULL STOP
    "ᠺ", # MONGGOLIAN LETTER KA
    "ᡮ", # MONGGOLIAN LETTER SIBE TSA
    "ᡟ", # MONGGOLIAN LETTER SIBE IY
    "ᡯ", # MONGGOLIAN LETTER SIBE ZA
    "ᡱ", # MONGGOLIAN LETTER SIBE CHA
    "ᡭ", # MONGGOLIAN LETTER SIBE HAA
    "", # MONGGOLIAN VOWEL SEPARATOR
    "ᡷ", # MONGGOLIAN LETTER MANCHU ZHA
]

INPUT_LAYER_SIZE = 50 * 350
WORD_MAX_CHARACTERS = 30
CHARACTERS_IN_ALPHABET = len(ALPHABET) # add one for empty chars
OUTPUT_LAYER_SIZE = WORD_MAX_CHARACTERS * CHARACTERS_IN_ALPHABET

class NeuralNetwork:
    LEARNING_RATE = 0.2
    _use_file = True
    NN_FILE_PATH = "saved_ann.json"

    def _rand_initialize_weights(self, size_in, size_out):
        return [((x * 0.12) - 0.06) for x in np.random.rand(size_out, size_in)]
    
    def _sigmoid_scalar(self, z):
        return 1 / (1 + math.e ** -z)
    
    def __init__(self, num_hidden_nodes):
        print("Initializing neural network")
        self.theta1 = self._rand_initialize_weights(INPUT_LAYER_SIZE, num_hidden_nodes)
        self.theta2 = self._rand_initialize_weights(num_hidden_nodes, OUTPUT_LAYER_SIZE)
        self.input_layer_bias = self._rand_initialize_weights(1, num_hidden_nodes)
        self.hidden_layer_bias = self._rand_initialize_weights(1, OUTPUT_LAYER_SIZE)
    
    def word_to_array(self, input_word):
        word = input_word.strip()
        array = [0] * OUTPUT_LAYER_SIZE
        for i in range(len(word)):
            char = word[i]
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

    def forward_propogate(self, pixel_string):
        pixels = [0] * INPUT_LAYER_SIZE
        for i in range(len(pixel_string)):
            char = pixel_string[i]
            if char == '1': pixels[i] = 1
        print(pixel_string, '\n', pixels)

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
    
    def back_propogate(self, pixels, results, actual_digit):
        y1 = results['y1']
        y2 = results['y2']

        actual_vals = [0] * OUTPUT_LAYER_SIZE
        actual_vals[actual_digit] = 1
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
        predictions = self.forward_propogate(test)['predictions']
   
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

    def train_on_example(self, pixels, actual_word):
        prediction = self.predict(pixels)
        pred_word = prediction["word"]
        pred_array = prediction["array"]
        self.back_propogate(pixels, pred_array, actual_word)
        print("Predicted {0}, actual word is {1}", pred_word, actual_word)
        return { "prediction": pred_word, "actual": actual_word }

    def train(self, training_data):
        predictions = []
        for example in training_data:
            prediction = self.train_on_example(example['image'], example['word'])
            predictions.append(prediction)
        return predictions
