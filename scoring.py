# Given an answer key (created with the manual_annotator) and the output from
# either the naive_classifier or commit_classifier, calculates the
# effectiveness of the classifier.

import sys

if __name__ == "__main__":
    correct = 0
    answers = []
    classified = []
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
            print "The classifier identified " + str(correct) + " commits correctly out of " + str(len(answers)) + " total commits."
            print "The classifier scored " + str(100 * float(correct)/float(len(answers))) + "%."
        else:
            print "ERROR: Lengths of answer key and classified commits incorrect."
    else:
        print "ERROR: Must use two arguments (python scoring {path_to_answer_key} {path_to_classifier_key})"
