# Classifer using nltk's NaiveBayesClassifier
# (This is what is described in the project proposal.)

import nltk
import os.path
import sys

def cwd():
    return os.path.dirname(os.path.dirname(__file__))

if __name__ == "__main__":

    # PREPARATION OF TRAINING DATA
    def get_words_in_commits(commits):
        all_words = []
        for (words, sentiment) in commits:
            all_words.extend(words)

        return all_words

    def get_word_features(word_list):
        word_list = nltk.FreqDist(word_list)
        word_features = word_list.keys()

        return word_features

    def extract_features(doc):
        doc_words = set(doc)

        features = {}
        for word in word_features:
            features['contains(%s)' % word] = (word in doc_words)

        return features

    answer_key = "data/fateanother_answer_key.txt"

    with open(answer_key, 'r') as f:
        answer_key = f.readlines()

        srs_commits = []
        fun_commits = []
        classification = ""
        for line in answer_key:
            if line == "serious\n":
                classification = line
                srs_commits.append((msg, classification))
            elif line == "funny\n":
                classification = line
                fun_commits.append((msg, classification))
            else:  # it's a commit message
                msg = line

        commits = []
        for (words, sentiment) in fun_commits + srs_commits:
            words_normalized = [w.lower() for w in words.split()]
            commits.append((words_normalized, sentiment))

        word_features = get_word_features(get_words_in_commits(commits))

        training_set = nltk.classify.apply_features(extract_features, commits[0])

