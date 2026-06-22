from ocr import NeuralNetwork
import json

def test_array_to_word():
    nn = NeuralNetwork(50)
    words = ["ᠮᡝᡵᡤᡝᠨ",
             "ᠮᡠᡨᡝᡵᡝ",
             "ᡨᡝᡵᡝ",
             "ᡨᡝᡵᡝ",]
    for word in words:
        array = nn.word_to_array(word)
        reconverted = nn.array_to_word(array)
        
        length = max(len(word), len(reconverted))
        for i in range(length):
            print(word[i], reconverted[i])

        assert word == reconverted

def test_predict_format():
    nn = NeuralNetwork(50)

    file = open("training_data.json", "r")
    raw_lines = file.readlines()[0:1]
    file.close()

    lines = []
    for line in raw_lines: lines.append(json.loads(line))

    for line in lines:
        prediction = nn.predict(line["image"])
        pred_array = prediction["array"]
        pred_word = prediction["word"]

        assert type(pred_array) == type([])
        assert type(pred_word) == type("string")
