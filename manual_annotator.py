# Given a .txt file such as "fateanother_commits.txt", will prompt the user
# to mark each commit message as either "funny" or "serious". Outputs a list of
# tuples of the form:

import argparse
import os.path
import re
import sys

def cwd():
    return os.path.dirname(os.path.dirname(__file__))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-file', action='store', type=str, help="fakerep_commits.txt", \
        default="data/fakerepo_commits.txt")

    args = parser.parse_args()
    answer_key = []

    input_file = cwd() + args.file
    output_file = args.file.split('_')[0] + '_answer_key.txt'

    with open(input_file, 'r') as f, open(output_file, 'w') as o:
        content = f.readlines()
        print "Mark commits as either (s)erious or (f)unny"
        for line in content:
            sys.stdout.write(line)  # display the next commit to classify
            classification = raw_input()

            while not re.match(r's|f', classification):
                print "Mark this commit as (s)erious or (f)unny"
                classification = raw_input()

            answer_key.append((line, classification))

        for answer in answer_key:
            o.write(str(answer) + '\n')
