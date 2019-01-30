import matplotlib
from sklearn.manifold import TSNE

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import gensim
import pandas as pd


def words_feeld(model, name):
    vocab = list(model.vocab)
    n = 50
    vocab2 = vocab[:n]
    print(vocab2)
    X = model[vocab]
    print(len(X))
    tsneplt = TSNE(n_components=2)
    X_tsne = tsneplt.fit_transform(X[:n, :])
    print(X_tsne)
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
    df = pd.DataFrame(X_tsne, index=vocab2, columns=['x', 'y'])
    print(df)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(df['x'], df['y'])
    for word, pos in df.iterrows():
        ax.annotate(word, pos)
    fig.savefig('../img/1' + name + '.png')


def closestwords(model, word, name):
    arr = np.empty((0, len(model[word])), dtype='f')
    word_labels = [word]

    close_words = model.similar_by_word(word)

    print(close_words)

    arr = np.append(arr, np.array([model[word]]), axis=0)

    for wrd_score in close_words:
        print(wrd_score[0])
        wrd_vector = model[wrd_score[0]]
        word_labels.append(wrd_score[0])
        arr = np.append(arr, np.array([wrd_vector]), axis=0)
    # find tsne coords for 2 dimensions
    tsne = TSNE(n_components=2)
    np.set_printoptions(suppress=True)
    X_tsne = tsne.fit_transform(arr)
    fig = plt.figure()
    x_coords = X_tsne[:, 0]
    y_coords = X_tsne[:, 1]
    plt.scatter(x_coords, y_coords)
    for label, x, y in zip(word_labels, x_coords, y_coords):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.xlim(x_coords.min() + 0.00005, x_coords.max() + 0.00005)
    plt.ylim(y_coords.min() + 0.00005, y_coords.max() + 0.00005)
    fig.savefig('../img/2' + name + '.png')


if __name__ == '__main__':
    test_word = "сылаас"

    modelPath_wiki = "../vectors/model.bin"
    modelPath_wiki_kyym = "../vectors/modelkyym.bin"

    model_wiki = gensim.models.KeyedVectors.load_word2vec_format(modelPath_wiki, binary=True)
    model_wiki_kyym = gensim.models.KeyedVectors.load_word2vec_format(modelPath_wiki_kyym, binary=True)


    closestwords(model_wiki, test_word, 'wiki')
    words_feeld(model_wiki, 'wiki')

    closestwords(model_wiki_kyym, test_word, 'wiki_kyym')
    words_feeld(model_wiki_kyym, 'wiki_kyym')
