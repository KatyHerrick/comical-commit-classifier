# Our customized classifier that we tweak to give better results
# than the NaiveBayesClassifier.
# (Including this empty file only if we get to this stage.)

import re, string

# SOME THINGS TO DO/WHERE I LEFT OFF:
# [x] 1. Remove punctuation for check_word_order_threshold test
# [] 2. Figure out best threshold
# [x] 3. Add loop through with punctuation to see if repeated punctuation
# [x] 4. Check for words in all CAPS LOCK
# [x] 5. Check without 's' at end of plural words. Causes a ton of false positives

# Obviously will be much longer, just a small list to start
automatic_funny = ['shit', 'fuck', 'ass', 'sucks', 'bad', 'garbage', 'awful',
    'terrible', 'damn', 'goddamn', 'dammit', 'goddammit', 'oops', 'lol', 'haha', 'retard',
    'retarded', 'geez', 'jeez', 'hahah', 'hahaha', 'fml', 'yolo', 'gg', 'idiot'
]

# Globals
table = string.maketrans("", "")

def remove_punctuation(s):
    return s.translate(table, string.punctuation)

def remove_letters(s):
    return s.translate(table, string.letters)

def remove_digits(s):
    return s.translate(table, string.digits)

def check_word_order_threshold(commit_word, dict_word):
    word_order_threshold = .82
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

if __name__ == '__main__':
    original_commits = []
    commits_for_write = {}
    commits_no_punc = []
    commits_with_caps = []
    commits_no_words = [] # Checking for multiple punctuation
    english_words = []
    with open('data/fateanother_commits.txt') as d:
        original_commits = d.readlines()
        commits_no_punc = [remove_punctuation(commit[1:].lower()).split('\n')[0].split(' ') for commit in original_commits]
        commits_with_caps = [remove_punctuation(commit[1:]).split('\n')[0].split(' ') for commit in original_commits]
        commits_no_words = [remove_digits(remove_letters(commit[1:])).split('\n')[0].split(' ') for commit in original_commits]
#    with open('english_word_list/google-10000-english-usa.txt') as w:
    with open('english_word_list/words2.txt') as w:
        english_words = [line.rstrip().lower() for line in w]

    count = 0
    for commit in original_commits:
        # Start commits_for_write dictionary
        count += 1
        cmt = ["Commit #" + str(count)]
        cmt.append(commit)
        commits_for_write[count] = cmt

    count = 0
    for commit in commits_no_punc:
        count += 1
        print "Commit #: " + str(count)
        for word in commit:
            if word in automatic_funny:
                cmt = commits_for_write[count]
                cmt.append('Is Funny\n')
                commits_for_write[count] = cmt
                print ' '.join(commit) + " ___ is funny"
                break
            if len(word) > 1 and (word[len(word)-1] == 's' or word[len(word)-1] == 'd'):
                # If last letter is 's', may be plural and not in english_words list
                if word[:len(word)-1] in english_words:
                    continue
            elif len(word) > 2 and word[len(word)-2:] == 'ed':
                if word[:len(word)-2] in english_words:
                    continue
            elif len(word) > 3 and word[len(word)-3:] == 'ing':
                if word[:len(word)-3] in english_words:
                    continue
            if not word in english_words:
            #and not word[:len(word)-1] in english_words:
                possible_typos = []
                not_a_typo = False
                for check_word in english_words:
                # Checking for typos
                    if len(check_word) >= len(word)-1 and len(check_word) <= len(word)-1:
                        # Might be a typo if word is within range 1 of length of word
                        test = check_word_order_threshold(word, check_word)
                        if test == True:
                            t = word + " is a possible typo of " + check_word
                            possible_typos.append(t)
                        if test == "BREAK":
                            break
                if possible_typos:
                    cmt = commits_for_write[count]
                    for typo in possible_typos:
                        cmt.append(typo + '\n')
                        print typo
                    commits_for_write[count] = cmt

    count = 0
    for commit in commits_with_caps:
        # Checking if there are commits with capital words
        count += 1
        for word in commit:
            if word.isupper():
                cmt = commits_for_write[count]
                cmt.append('Is Funny\n')
                commits_for_write[count] = cmt

    count = 0
    for commit in commits_no_words:
        # Checking if there are commits with repeated punctuation
        count += 1
        for punc in commit:
            if len(punc) > 1:
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