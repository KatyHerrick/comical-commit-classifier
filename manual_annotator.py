# Given a .txt file such as "fateanother_commits.txt", will prompt the user
# to mark each commit message as either "funny" or "serious". Outputs a list of
# tuples of the form:

import argparse
import os.path

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
        for line in content:
            print line + "\n"