# Given a .txt file such as "fateanother_raw_logs.txt", will output a .txt file
# of only the commit messages, separated by a newline character.

import argparse
import os.path

def cwd():
    return os.path.dirname(os.path.dirname(__file__))

def read_file(input_file):
    raw_logs = input_file.readlines()
    raw_logs = [line for line in raw_logs if line != '\n']
    raw_logs.append('END_OF_LOGS')

    return raw_logs

def should_concatenate(line):
    """
    Re-evaluate if the program should start concatenating the commit again. Returns
    a boolean True if one of the following conditions is true:
        1) the line does not start with one of the key words
        2) the line starts with the word "commit", but isn't simply the commit number

    A regex to determine if a line is a commit message starting with the word "commit"
    rather than the commit number would be preferable to this method.
    """
    line_starts_to_ignore = ['commit', 'Merge:', 'Author:', 'Date:', 'END_OF_LOGS']

    return line[0] not in line_starts_to_ignore or \
        (line[0] == "commit" and len(line) > 2)

def make_commit_list(raw_logs):
    line_starts_to_ignore = ['commit', 'Merge:', 'Author:', 'Date:', 'END_OF_LOGS']

    commits = []
    commit = ""
    concatenating = False

    for line in raw_logs:
        line = line.split()
        if not concatenating:
            concatenating = should_concatenate(line)

        if concatenating:
            if not line:
                pass  # ignore empty lines
            elif line[0] in line_starts_to_ignore and len(line) <= 2:  # indicates next commit has started
                commits.append(commit)
                concatenating = False
                commit = ''
            else:
                line = ' '.join(line)
                commit += line

    return commits

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-log', action='store', type=str, help="repo_name_raw_logs.txt", \
        default="data/fakerepo_raw_logs.txt")

    args = parser.parse_args()

    input_file = cwd() + args.log
    output_file = args.log.split('_')[0] + '_commits.txt'
    with open(input_file, 'r') as f, open(output_file, 'w') as o:

        raw_logs = read_file(f)

        commits = make_commit_list(raw_logs)

        for commit in commits:
            o.write(commit + '\n')
