import nltk
import csv
from nltk.corpus import stopwords


def read_faq_from_file(file_path):
    file = open(file_path, 'r')
    return file.read()


def remove_punctuations_and_lemmatize(words):
    wnl = nltk.WordNetLemmatizer()
    return [wnl.lemmatize(word) for word in words if word.isalpha()]


def score_words(text):
    words_in_text = nltk.word_tokenize(text)
    # words = remove_punctuations_and_lemmatize(words_in_text)
    stop_words = set(stopwords.words('english'))
    freq_table = dict()
    for word in words_in_text:
        if word in stop_words:
            continue
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1
    return freq_table


def score_sentences(sentences, word_freq_table):
    sentence_score = dict()
    for sentence in sentences:
        word_count = len(nltk.word_tokenize(sentence))
        for word in word_freq_table:
            if word in sentence.lower():
                short_sent = sentence[:100]
                if short_sent in sentence_score:
                    sentence_score[short_sent] += word_freq_table[word]
                else:
                    sentence_score[short_sent] = word_freq_table[word]
    return sentence_score


def find_threshold(score_table):
    sum_score = 0
    for score in score_table:
        sum_score += score_table[score]
    average = int(sum_score / len(score_table))
    return average * 1.5


def generate_summary(sentences, sentence_score_table, threshold):
    sentence_count = 0
    summary = ''
    for sentence in sentences:
        short_sent = sentence[:100]
        if sentence_score_table[short_sent] > threshold:
            summary += ' ' + sentence
            sentence_count += 1
    print('sentence count in summary: ', sentence_count)
    return summary


def main():
    paragraph = read_faq_from_file('E:/PyCharm Workspace/faqbot/resources/textSummarization/paragraph.txt')
    word_freq_table = score_words(paragraph)
    sentences = nltk.sent_tokenize(paragraph)
    print('sentence count in paragraph: ', len(sentences))
    sentence_score_table = score_sentences(sentences, word_freq_table)
    print('sentence score table: ', sentence_score_table)
    score_threshold = find_threshold(sentence_score_table)
    print('score threshold', score_threshold)
    summary = generate_summary(sentences, sentence_score_table, score_threshold)
    print(summary)


if __name__ == '__main__':
    main()

