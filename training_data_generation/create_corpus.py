corpus = []

def get_lines():
    file = open("Jerry_Norman_Dict.txt", "r")
    lines = file.readlines()
    file.close()
    return lines

def line_is_empty(line):
    return len(line) <= 1

def get_manchu_words(line):
    words = line.split(" ")
    manchu_words = []
    for word in words:
        if word.isupper():
            manchu_words.append(word)
        else:
            return manchu_words
    return manchu_words

def add_to_corpus(word):
    if word in corpus:
        return
    corpus.append(word)
    return

def save_corpus():
    with open("corpus.txt", "w", encoding="utf-8") as file:
        for word in corpus:
            file.write(word + "\n")

def main():
    lines = get_lines()

    for line in lines:
        if line_is_empty(line):
            continue
    
        manchu_words = get_manchu_words(line)
        for word in manchu_words:
            add_to_corpus(word)

    print(corpus)
    print(str(len(corpus)) + " words in corpus")
    save_corpus()

if __name__ == "__main__":
    main()
