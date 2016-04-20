# Given a .txt file such as "fateanother_commits.txt", will prompt the user
# to mark each commit message as either "funny" or "serious". Outputs a list of
# tuples of the form:

import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-file', action='store', type=str, help="fakerep_commits.txt", \
        default="data/fakerepo_commits.txt")

    args = parser.parse_args()

    with open(args.file) as f:
        content = f.readlines()
        for line in content:
            print line + "\n"