# Converts old ('sentence', 'classification') syntax to:
# Line 1: sentence
# Line 2: classification
# ...

answer_key = 'data/fateanother_answer_key.txt'
new_key = 'data/fateanother_answer_key_2.txt'

answer_key_lines = []
new_key_lines = []

with open(answer_key, 'r') as a:
    answer_key_lines = a.readlines() 

with open(new_key, 'w') as n:
    for x in range(0, len(answer_key_lines)):
        answer_key_lines[x] = answer_key_lines[x][3:]
        temp = answer_key_lines[x].split("\\n'")
        if not len(temp) == 2:
            temp = answer_key_lines[x].split('\\n"')
        sentence = temp[0]
        classification = temp[1][3:]
        classification = classification[:len(classification)-3]
        n.write(sentence + '\n')
        n.write(classification + '\n')
