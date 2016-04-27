# Classifer using nltk's NaiveBayesClassifier
# (This is what is described in the project proposal.)

import nltk
import os.path

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
        word_features = wordList.keys()

        return word_features

    def extract_features(doc):
        doc_words = set(doc)

        features = {}
        for word in word_features:
            features['contains(%s)' % word] = (word in doc_words)

        return features

    fun_commits = [(' Half finished combo, misc changes Tried illusion approach but it was being goddamn complex and gimmicky as usual. RIP 3 hours If everything goes well Ruler should be ready for release tomorrow evening, although my crunch will have to continue for some attribute reworks and system changes T_T\n', 'funny'),
        (' holy shit i\'m bad at literally everything\n', 'funny'),
        (' Added some basic spellcasting whatever the fuck :)\n', 'funny',
        (' v1.38b uh oh spaghettios\n', 'funny'),
        (' Better Gate Texture cuz the lightning looked like shit\n', 'funny')
    ]

    srs_commits = [(' v1.38\n', 'serious'),
    (' Updated to pause mechanism and Rider particle - No longer restricts command, meaning you can queue ability while in casting - Beams now release towards direction caster is heading at the fire - Removed ground spike from Bellerophon and smoke from Nail Swing\n', 'serious'),
    (" Fixed a bug with Archer and updated Avenger's skill template - Fixed a bug where UBW weapons would remain after round ended and damage enemy heroes at respawn\n", 'serious'),
    (' first commit first commit 123 Revert "asd" This reverts commit 79dcd48bd6b917049fa850be1be217809fbc4636. asd first commit scripts Scripts\n', 'serious'),
    (' Merge pull request #21 from F1l00/master Casster (Extra) Sound Script\n', 'serious')]

    commits = []
    for (words, sentiment) in fun_commits + srs_commits:
        words_normalized = [w.lower() for w in words.split()]
        commits.append((words_normalized, sentiment))

    word_features = get_word_features(get_words_in_commits(commits))

    training_set = nltk.classify.apply_features(extract_features, commits[0])
    print training_set


    # MAKING THE CLASSIFIER
    # if sys.argv[1]:
    #     commit_file = sys.argv[1]
    # else:
    #     commit_file = "data/fateanother_commits.txt"

    # with open(commit_file, 'r') as f:
    #     commits = commit_file.readlines()
