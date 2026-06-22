from ocr import NeuralNetwork

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
