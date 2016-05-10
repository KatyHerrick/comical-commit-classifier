# Our customized classifier that we tweak to give better results
# than the NaiveBayesClassifier.
# (Including this empty file only if we get to this stage.)

import re, string, sys

# Words that will make a commit automatically funny
automatic_funny = ['shit', 'fuck', 'ass', 'sucks', 'bad', 'garbage', 'awful',
    'terrible', 'damn', 'goddamn', 'dammit', 'goddammit', 'oops', 'lol', 'haha', 'retard',
    'retarded', 'geez', 'jeez', 'hahah', 'hahaha', 'fml', 'yolo', 'gg', 'idiot',
    'clusterfuck', 'dead', 'fml', 'fucker', 'fucked', 'god', 'hate', 'mess', 'piss', 
    'shitcode', 'sorry', 'stupid', 'trash', 'ugh', 'whoops', 'holy',
]

# Globals
table = string.maketrans("", "")

def remove_punctuation(s):
    return s.translate(table, string.punctuation)

def remove_letters(s):
    return s.translate(table, string.letters)

def remove_digits(s):
    return s.translate(table, string.digits)

# Checks how closely spelled two words are
def check_word_order_threshold(commit_word, dict_word):
    word_order_threshold = .875
    word_count = 0
    shorter_word_length = 0
    if len(commit_word) < len(dict_word):
        shorter_word_length = len(commit_word)
    else:
        shorter_word_length = len(dict_word)
    for x in range(0, shorter_word_length):
        if commit_word[x] == dict_word[x]:
            word_count += 1
    if word_count == shorter_word_length:
        # If every letter of the commit_word is in order with dict_word
        # that most likely suggests commit_word is simply a subset of
        # dict_word, not a typo
        return "BREAK" 
    word_order_test = float(word_count) / float(len(dict_word))
    if word_order_test > word_order_threshold:
        return True
    return False

def check_s_d(word, english_words):
    # If last letter is 's' or 'd', may be plural and not in english_words list
    if len(word) > 1 and (word[len(word)-1] == 's' or word[len(word)-1] == 'd'):
        if word[:len(word)-1] in english_words:
            return True
    return False

def check_ed(word, english_words):
    if len(word) > 2 and word[len(word)-2:] == 'ed':
        if word[:len(word)-2] in english_words:
            return True
    return False

def check_ing(word, english_words):
    if len(word) > 3 and word[len(word)-3:] == 'ing':
        if word[:len(word)-3] in english_words:
            return True
    return False

def is_typo(typo_list):
    typo_count = {}
    word_is_typo = []
    if typo_list:
        # If there are typos, figure out if it's actually a typo.
        # Does it exist multiple times in repo?
        for key in typo_list:
            word_list = {}
            possible_typos = typo_list[key]
            for typo in possible_typos:
                if typo in word_list:
                    word_list[typo] += 1
                else:
                    word_list[typo] = 1
            typo_count[key] = word_list
    if typo_count:
        for key in typo_count:
            word_list = typo_count[key]
            for word in word_list:
                if not word_list[word] > 1:
                    # Is a typo
                    if not key in word_is_typo:
                        word_is_typo.append(key)
    return word_is_typo

def commit_is_funny(word_is_typo, commits_for_write):
    for key in commits_for_write:
        for word in word_is_typo:
            array = commits_for_write[key]
            for line in array:
                if word in line:
                    commits_for_write[key].append("Is Funny\n")
    return commits_for_write
                

if __name__ == '__main__':
    original_commits = []
    commits_for_write = {} 
    commits_no_punc = []
    commits_with_caps = []
    commits_no_words = [] # Checking for multiple punctuation
    english_words = []
    typo_list = {} 

    if len(sys.argv) < 2:
        print "ERROR: please add argument for repository (python commit_classifier.py {path_to_repository}"
        exit()
    path_to_commits = sys.argv[1]

    with open(path_to_commits) as d:
        original_commits = d.readlines()
        commits_no_punc = [remove_punctuation(commit[1:].lower()).split('\n')[0].split(' ') for commit in original_commits] 
        commits_with_caps = [remove_punctuation(commit[1:]).split('\n')[0].split(' ') for commit in original_commits]
        commits_no_words = [remove_digits(remove_letters(commit[1:])).split('\n')[0].split(' ') for commit in original_commits]
    with open('english_word_list/words2.txt') as w:
        english_words = [line.rstrip().lower() for line in w]

    count = 0
    for commit in original_commits:
        # Start commits_for_write dictionary
        count += 1
        cmt = ["Commit #" + str(count)]
        cmt.append(commit)
        commits_for_write[count] = cmt

    # Checking for typos
    count = 0
    for commit in commits_no_punc:
        count += 1
        print "Commit #: " + str(count)
        for word in commit:
            if word in automatic_funny:
                cmt = commits_for_write[count]
                cmt.append('Is Funny\n')
                commits_for_write[count] = cmt
                #print ' '.join(commit) + " ___ is funny"
                break
            if word == 'Merge':
                break
            if check_s_d(word, english_words):
                continue
            elif check_ed(word, english_words):
                continue
            elif check_ing(word, english_words):
                continue
            if not word in english_words: 
                not_a_typo = False
                for check_word in english_words:
                # Checking for typos
                    if len(check_word) >= len(word)-1 and len(check_word) <= len(word)-1:
                        # Might be a typo if word is within range 1 of length of word
                        test = check_word_order_threshold(word, check_word)
                        if test == True:
                            if word in typo_list:
                                temp = typo_list[word]
                                temp.append(check_word)
                                typo_list[word] = temp
                            else:
                                typo_list[word] = [check_word]
                        if test == "BREAK":
                            break

    word_is_typo = is_typo(typo_list)
    commits_for_write = commit_is_funny(word_is_typo, commits_for_write) 

    count = 0
    for commit in commits_with_caps:
        # Checking if there are commits with capital words
        count += 1
        for word in commit:
            if word.isupper() and len(word) > 3:
                cmt = commits_for_write[count]
                cmt.append('Is Funny\n')
                commits_for_write[count] = cmt

    count = 0
    for commit in commits_no_words:
        # Checking if there are commits with repeated punctuation
        count += 1
        for punc in commit:
            if len(punc) > 4:
                cmt = commits_for_write[count]
                cmt.append('Is Funny\n')
                commits_for_write[count] = cmt

    a = open('classifier_answers.txt', 'w')
    f = open('classifier_output.txt', 'w')
    for key in commits_for_write:
        info = commits_for_write[key]
        is_funny = "Is Funny\n"
        if is_funny in info: 
            a.write(info[1][1:])
            a.write('funny\n')
        else:
            a.write(info[1][1:])
            a.write('serious\n')
        for data in info:
            f.write(data)
    f.close()
    a.close()
