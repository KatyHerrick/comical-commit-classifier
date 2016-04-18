# Given a .txt file such as "fateanother_raw_logs.txt", will output a .txt file
# of only the commit messages, separated by a newline character.

import argparse
import os.path

def cwd():
    return os.path.dirname(os.path.dirname(__file__))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Cleans unaltered git log output for classification')
    parser.add_argument('-log', action='store', type=str, help="repo_name_raw_logs.txt", default="data/fateanother_raw_logs.txt")

    args = parser.parse_args()

    with open(cwd() + args.log) as f:
        print f.read()
