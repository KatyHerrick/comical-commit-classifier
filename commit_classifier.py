# Our customized classifier that we tweak to give better results
# than the NaiveBayesClassifier.
# (Including this empty file only if we get to this stage.)

# SOME THINGS TO DO/WHERE I LEFT OFF:
# 1. Remove punctuation for check_word_order_threshold test
# 2. Figure out best threshold
# 3. Add loop through with punctuation to see if repeated punctuation
# 4. Check for words in all CAPS LOCK
# 5. Check without 's' at end of plural words. Causes a ton of false positives 

# Obviously will be much longer, just a small list to start
automatic_funny = ['shit', 'fuck', 'ass', 'sucks', 'bad', 'garbage', 'awful',
    'terrible', 'damn', 'goddamn', 'dammit', 'goddammit', 'oops', 'lol', 'haha', 'retard',
    'retarded', 'geez', 'jeez', 'hahah', 'hahaha', 'fml', 'yolo', 'gg', 'idiot'
]

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
    commits = []
    english_words = []
    count = 0
    with open('data/fateanother_commits.txt') as d:
        temp_words = d.readlines()
        commits = [commit[1:].lower().split('\n')[0].split(' ') for commit in temp_words] 
    with open('english_word_list/words2.txt') as w:
        english_words = [line.rstrip().lower() for line in w]
    for commit in commits:
        temp = False
        count += 1
        print "Commit #: " + str(count)
        for word in commit:
            if word in automatic_funny:
                print ' '.join(commit) + " ___ is funny"
                break
            if not word in english_words or not word[:-1] in english_words:
                for check_word in english_words:
                    if len(check_word) >= len(word)-1 and len(check_word) <= len(word)-1:
                        test = check_word_order_threshold(word, check_word)
                        if test == True:
                            #print "Full word: " + check_word + " Commit word: " + word
                            break
                        if test == "BREAK":
                            break
