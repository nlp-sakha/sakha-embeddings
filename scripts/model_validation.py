import sys

import matplotlib
from sklearn.manifold import TSNE

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import gensim
import pandas as pd

from config_to_model_validation import SAMPLE_2, SAMPLE_4, SAMPLE_5

modelPath_wiki = "../vectors/model.bin"
modelPath_wiki_kyym = "../vectors/modelkyym.bin"

model_wiki = gensim.models.KeyedVectors.load_word2vec_format(modelPath_wiki, binary=True)
model_wiki_kyym = gensim.models.KeyedVectors.load_word2vec_format(modelPath_wiki_kyym, binary=True)

print('Pls enter how many words you want see in figure integer number')
n = int(input())

if (n > 10000 or n < 0):
    print('Not validet please enter number from n < 10000 and n >0')
    sys.exit()


def words_feeld(model, name, n):
    vocab = list(model.vocab)
    vocab2 = vocab[:n]
    X = model[vocab]
    tsneplt = TSNE(n_components=2)
    X_tsne = tsneplt.fit_transform(X[:n, :])
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
    df = pd.DataFrame(X_tsne, index=vocab2, columns=['x', 'y'])
    fig = plt.figure(num=None, figsize=(100, 100), dpi=150, facecolor='w', edgecolor='k')
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(name, fontsize=120)
    ax.scatter(df['x'], df['y'])
    for word, pos in df.iterrows():
        ax.annotate(word, pos)
    fig.savefig('../img/' + name + '.png')
    ax.clear()
    fig.clf()


words_feeld(model_wiki, 'wiki', n)
words_feeld(model_wiki_kyym, 'wiki_kyym', n)

print('finish create big picture')


def kinship(sample_1, sample_2, sample_3, model, name):
    bigsample = sample_1 + sample_2 + sample_3
    X = model[bigsample]
    tsneplt = TSNE(n_components=2)
    X_tsne = tsneplt.fit_transform(X[:len(bigsample), :])
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
    df = pd.DataFrame(X_tsne, index=bigsample, columns=['x', 'y'])
    # print(df)
    fig = plt.figure(num=1, figsize=(10, 10), dpi=150, facecolor='w', edgecolor='k')
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(name)
    ax.scatter(df['x'], df['y'])

    print(df.take([0, 1]))
    print(df.take([2, 3]))
    print(df.take([4, 5]))

    xes = [df.iloc[0]['x'], df.iloc[1]['x']]
    yes = [df.iloc[0]['y'], df.iloc[1]['y']]
    plt.plot(xes, yes)

    xes1 = [df.iloc[2]['x'], df.iloc[3]['x']]
    yes1 = [df.iloc[2]['y'], df.iloc[3]['y']]
    plt.plot(xes1, yes1)

    xes2 = [df.iloc[4]['x'], df.iloc[5]['x']]
    yes3 = [df.iloc[4]['y'], df.iloc[5]['y']]
    plt.plot(xes2, yes3)

    for word, pos in df.iterrows():
        ax.annotate(word, pos)

    fig.savefig('../img/model_valid_vectors_' + name + '.png')
    ax.clear()
    fig.clf()


kinship(SAMPLE_5, SAMPLE_4, SAMPLE_2, model_wiki, 'wiki')

kinship(SAMPLE_5, SAMPLE_4, SAMPLE_2, model_wiki_kyym, 'wiki_kyym')
