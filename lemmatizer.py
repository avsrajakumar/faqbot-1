from nltk.stem import WordNetLemmatizer

from file_reader import read_file
from noise_remover import perf_noise_cancelling


def lemmatize(words):
    lemmatizer = WordNetLemmatizer()
    result = []
    # TODO: use appropriate POS
    for word in words:
        result.append(lemmatizer.lemmatize(word))

    return result


def main():
    words = perf_noise_cancelling(read_file("./resources/titanic.txt", "r"))
    print(lemmatize(words))


if __name__ == '__main__':
    main()
