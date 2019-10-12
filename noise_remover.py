import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords

# read file
file = open("./resources/titanic.txt", "r")
content = file.read()
print("Content: ", content)

# tokenize
words = nltk.word_tokenize(content)
without_stopwords = []

# filter
for word in words:
    if word not in stopwords.words('english') and word.isalpha():
        without_stopwords.append(word)

# display
print("Without stop words: ", without_stopwords)
