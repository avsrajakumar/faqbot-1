#reference
#https://medium.com/@adriensieg/text-similarities-da019229c894
#https://datascience.stackexchange.com/questions/23969/sentence-similarity-prediction
import nltk
from gensim import models

def avg_feature_vector(words, model, num_features, index2word_set):
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0
    for word in words:
        if word in index2word_set:
            nwords = nwords + 1
            featureVec = np.add(featureVec, model[word])

    if nwords > 0:
        featureVec = np.divide(featureVec, nwords)
    return featureVec


sentence_1 = "this is sentence number one"
sentence_1_avg_vector = avg_feature_vector(sentence_1.split(), model=word2vec_model, num_features=100)

# get average vector for sentence 2
sentence_2 = "this is sentence number two"
sentence_2_avg_vector = avg_feature_vector(sentence_2.split(), model=word2vec_model, num_features=100)

sen1_sen2_similarity = cosine_similarity(sentence_1_avg_vector, sentence_2_avg_vector)
