import nltk
nltk.download("stopwords")

from nltk.corpus import stopwords
from file_reader import read_file


def perf_noise_cancelling(content):
    words = nltk.word_tokenize(content)
    without_stopwords = []

    for word in words:
        if word not in stopwords.words('english') and word.isalpha():
            without_stopwords.append(word)

    print("Without stop words: ", without_stopwords)


def main():
    content = read_file("./resources/titanic.txt", "r")
    perf_noise_cancelling(content)


if __name__ == '__main__':
    main()
