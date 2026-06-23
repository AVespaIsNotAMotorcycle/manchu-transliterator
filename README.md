# marina-samuel-ocr

An extension of [a previous OCR project](https://github.com/AVespaIsNotAMotorcycle/marina-samuel-ocr)
to recognition of Manchu text.

## Training Data

In order to generate large amounts of training data, a large corpus of words is rendered as images in
various fonts. Each word has - as of now - eleven variations. The words were pulled from
[manchu-cake](https://github.com/OverflowCat/manchu-cake).

<img width="1858" height="1053" alt="Screenshot From 2026-06-18 12-05-26" src="https://github.com/user-attachments/assets/57929c0c-419f-42d1-bc4d-903f57ab2e4e" />

## Processing

### Attempt One: The Whole Image

An initial, simple attempt at processing the input was to simply look at the entire image and generate a length `x * y` array, where `x` is the length of the longest word plus some padding (I chose 30 characters), and `y` is the number of characters in the alphabet (39 if you include whitespace). After being trained on 51,358 words, the results were bad. The ANN's predictions of the length of the string were off by about 3%, and it correctly identified about 20% of the characters within any given word.

<img width="888" height="549" alt="chart(1)" src="https://github.com/user-attachments/assets/4b43d281-1b6e-4bb2-b9e0-ee91cb90bcb1" />

### Attempt Two: Without the Center Line

Manchu words are written with all the letters joined by a vertical line. However, what really conveys information is what's on either side of the line (or where it disappears). Now the ANN would detect and remove the center line from images before attempting to read them.

<img width="1081" height="887" alt="image" src="https://github.com/user-attachments/assets/adde2d6a-763b-42a5-92d5-73270c052b17" />

This resulted in a modest performance increase, from 20% of characters correctly identified to 24%.

<img width="1008" height="623" alt="chart(4)" src="https://github.com/user-attachments/assets/8967f9a6-ce71-4664-b7a2-39ab754bf175" />

