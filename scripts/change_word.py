import gensim
from word2vec_conf import NOT_CHANGE_WORD

modelPath_wiki = "../vectors/all.bin"
model = gensim.models.KeyedVectors.load_word2vec_format(modelPath_wiki, binary=True)

not_change_word = NOT_CHANGE_WORD

new_sentence = []
accuracy = 0

with open('./sentence.txt') as f:
    lines = f.read().split()

enter_text = ' '.join(lines)
print('enter sentence: ' + str(enter_text))

for elem in lines:
    if elem in not_change_word:
        new_sentence.append(elem)
        accuracy += 1
    else:
        w1 = elem
        out_word = model.most_similar(positive=w1, topn=1)
        new_sentence.append(out_word[0][0])
        accuracy += out_word[0][1]

out_text = ' '.join(new_sentence)
out_accuracy = accuracy / len(lines)
print('out sentence: ' + str(out_text))
print('accuracy: ' + str(out_accuracy))
