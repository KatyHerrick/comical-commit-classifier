# Given a .txt file such as "fateanother_raw_logs.txt", will output a .txt file
# of only the commit messages, separated by a newline character.

import argparse
import os.path

def cwd():
    return os.path.dirname(os.path.dirname(__file__))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Cleans unaltered git log output for classification')
    parser.add_argument('-log', action='store', type=str, help="repo_name_raw_logs.txt", default="data/fakelogs_raw_logs.txt")

    args = parser.parse_args()

    with open(cwd() + args.log) as f:
        line_starts_to_ignore = ['commit', 'Merge: ', 'Author:', 'Date:']
        raw_logs = f.readlines()
        raw_logs = [line for line in raw_logs if line != '\n']

        commits = []
        commit = ""
        concatenating = False

        for line in raw_logs:
            line = line.split()
            if not concatenating:
                if line[0] not in line_starts_to_ignore:
                    concatenating = True

            if concatenating:
                if line[0] in line_starts_to_ignore:  # indicates next commit has started
                    commits.append(commit)
                    concatenating = False
                    commit = ""
                else:
                    line = ' '.join(line)
                    commit = commit + ' ' + line
        print commits

        ## To do: make a temp array for commits to reconsitute multiline commits
