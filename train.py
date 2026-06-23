from ocr import NeuralNetwork
import json
import random

def get_training_data(start, end):
    print("Loading training data...")
    file = open("training_data.json", "r")
    raw_lines = file.readlines()
    lines = []
    for index in range(start, end):
        try:
            line = raw_lines[index]
            lines.append(json.loads(line))
        except: continue
    print("Loaded training data.")
    return lines

def print_progress(examples, predictions):
    print("Logging results...")
    logs = []
    for index in range(len(examples)):
        example = examples[index]
        prediction = predictions[index]

        actual_word = example["word"]
        predicted_word = prediction["prediction"]
        correct = actual_word == predicted_word
        logs.append({ "actual": actual_word, "predicted": predicted_word, "correct": correct })

def train():
    print("Initializing neural network...")
    nn = NeuralNetwork(100)

    examples = get_training_data(0, 3000)
    print("Training...")
    random.shuffle(examples)
    predictions = nn.train(examples)
    print("Trained.")
    print_progress(examples, predictions)

    nn.save()

train()
