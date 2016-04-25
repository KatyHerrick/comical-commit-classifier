# Given an answer key (created with the manual_annotator) and the output from
# either the naive_classifier or commit_classifier, calculates the
# effectiveness of the classifier.

import re
import sys

if __name__ == "__main__":
    correct = 0
    if sys.argv[1] and sys.argv[2]:
        answer_key = sys.argv[1]
        classifier = sys.argv[2]
        with open(answer_key, 'r') as a, open(classifier, 'r') as c:
            answers = a.readlines()
            classified = c.readlines()
        if len(answers) == len(classified):
            for x in range(1, len(answers)):
                if answers[x-1] == classified[x-1]:
                    correct += 1      
            print "The classifier identified " + correct + " commits correctly out of " + len(answers) + " total commits."
            print "The classifier scored " + correct/len(answers + "%."
        else:
            print "ERROR: Lengths of answer key and classified commits incorrect."
    else:
        print "ERROR: Must use two arguments (python scoring {path_to_answer_key} {path_to_classifier_key})"
