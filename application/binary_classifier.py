import csv
import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn import preprocessing
from nltk.corpus import wordnet as wn
from sklearn.naive_bayes import MultinomialNB
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


class TechnicalClassifier:
    def __init__(self, file, g_file):
        self.word_net_lemma = WordNetLemmatizer()
        self.stop_words = list(set(stopwords.words('english')))
        self.stop_words.append('?')
        self.stop_words.append('name')
        self.stem_obj = SnowballStemmer('english')
        self.le = preprocessing.LabelEncoder()
        self.cv = CountVectorizer(ngram_range=(1, 1), lowercase=True)
        self.tf_idf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
        self.clf = MultinomialNB(alpha=0.6, fit_prior=False)
        self.raw_questions = []
        self.raw_categories = []
        self.raw_category_question = []
        self.file = file
        self.g_file = g_file
        self.X = []
        self.y = []
        self.read_file(self.file)
        self.read_file_generic(self.g_file)

    def initialize_models(self):
        questions = np.array([self.pre_process_question(q) for q in self.raw_questions])
        word_count_vector = self.cv.fit_transform(questions)
        self.tf_idf_transformer.fit(word_count_vector)
        feature_names = self.cv.get_feature_names()
        tf_idf_vector = self.tf_idf_transformer.transform(word_count_vector)
        vector = [np.squeeze(np.asarray(v.T.todense())) for v in tf_idf_vector]
        vector = np.array(vector)
        self.le.fit(self.raw_categories)
        self.X = vector
        self.y = np.array(self.le.transform(self.raw_categories))
        self.clf.fit(self.X, self.y)

    def read_file(self, file):
        with open(self.file) as file:
            csv_reader = csv.reader(file, delimiter='\t')
            for each_line in csv_reader:
                category = 'Generic' if each_line[0] == 'Generic' else 'Technical'
                self.raw_questions.append(each_line[1])
                self.raw_categories.append(category)
                self.raw_category_question.append((each_line[0], each_line[1]))
        # self.raw_questions = np.array(self.raw_questions)
        # self.raw_categories = np.array(self.raw_categories)

    def read_file_generic(self, g_file):
        with open(g_file) as file:
            csv_reader = csv.reader(file)
            counter = 0
            for each_line in csv_reader:
                each_line = each_line[0].split('+++$+++')
                self.raw_questions.append(each_line[1])
                self.raw_categories.append(each_line[0])
                self.raw_category_question.append((each_line[0], each_line[1]))
        self.raw_questions = np.array(self.raw_questions)
        self.raw_categories = np.array(self.raw_categories)

    def pre_process_question(self, sent):
        words = [self.stem_obj.stem(w.lower()) for w in word_tokenize(sent) if self.stem_obj.stem(w.lower()) not in self.stop_words]
        result = []
        for w in words:
            synsets = wn.synsets(self.word_net_lemma.lemmatize(w))
            if len(synsets) > 0:
                name = synsets[0].name()
                if '.' in name:
                    result.append(name.split('.')[0])
                else:
                    result.append(name)
            else:
                if '.' in w:
                    w = w.split('.')[0]
                result.append(w)
        return " ".join(result)

    def get_technical_category(self, question):
        question = self.pre_process_question(question)
        if len(question) == 0:
            return 'Generic'
        X = self.tf_idf_transformer.transform(self.cv.transform([question]))
        X = np.squeeze(np.asarray(X.T.todense()))
        X = np.array(X)
        X = self.clf.predict([X])
        return self.le.inverse_transform(X)[0]

    def get_questions(self, category=None):
        if category is None:
            return category
        else:
            res = [q for c, q in self.raw_category_question if c == category]
            return res
'''
if __name__ == '__main__':
    tc = TechnicalClassifier('resources/Single_FaQ.csv', 'resources/generic_diag.csv')
    tc.initialize_models()

    while True:
        question = input('Question: ')
        result = tc.get_technical_category(question)
        print('{}'.format(result))
'''

