import argparse
import gzip
import logging
import os

import gensim
from word2vec_conf import EPOCHS

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)



# with dlya raboti s neupravlyami resursami
# enumerate avtomaticheski shet4ik prostavlyat zna4enie v strokah listah ili massivah
def show_file_contents(input_file):
    with gzip.open(input_file, 'rb') as f:
        for i, line in enumerate(f):
            # print(line)
            break


def read_input(input_file, gzip=True):
    """This method reads the input file which is in gzip format"""

    logging.info("reading file {0}...this may take a while".format(input_file))
    if gzip == True:
        with gzip.open(input_file, 'rb') as f:
            for i, line in enumerate(f):

                if (i % 1000 == 0):
                    logging.info("read {0} reviews".format(i))
                # do some pre-processing and return list of words for each review
                # text
                yield gensim.utils.simple_preprocess(line)
    else:
        with open(input_file, 'rb') as f:
            for i, line in enumerate(f):

                if (i % 1000 == 0):
                    logging.info("read {0} reviews".format(i))
                # do some pre-processing and return list of words for each review
                # text
                yield gensim.utils.simple_preprocess(line)


def main(input_file='data/all.txt', output_file='vectors/all.bin'):
    abspath = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(abspath, input_file)
    # print(abspath)
    # text = io.open(abspath + '/wiki.sakha.txt', 'r', encoding='utf-8').read()

    # read the tokenized reviews into a list
    # each review item becomes a serries of words
    # so this becomes a list of lists
    documents = list(read_input(data_file, gzip=False))
    # print(documents)
    # sys.exit(1)
    logging.info("Done reading data file")

    # build vocabulary and train model
    model = gensim.models.Word2Vec(
        documents,
        size=150,
        window=10,
        min_count=2,
        workers=10)
    model.train(documents, total_examples=len(documents), epochs=EPOCHS)

    # save only the word vectors
    model.wv.save_word2vec_format(output_file, binary=True)
    # model.wv.save(os.path.join(abspath, "../vectors/defaultsakha.kv"))

    # look up top 6 words similar to 'polite'
    w1 = ["кыыл"]
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            topn=6))
    w1 = ["суруйаачыта"]
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            topn=6))
    w1 = ["куорат"]
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            topn=6))
    w1 = ["маҥан"]
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            topn=6))
    w1 = ["сырдык"]
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            topn=6))
    w1 = ["сүүрэр"]
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            topn=6))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Utilit for parsing some websites '
                                                    'with sakha language content')
    argparser.add_argument('-c',
                           '--corpus',
                           type=str,
                           help='Path to corpus file',
                           required=True)

    argparser.add_argument('-o',
                           '--output',
                           type=str,
                           help='Path to output model, ',
                           default='vectors/model.bin',
                           required=True)

    args = argparser.parse_args()

    main(input_file=args.corpus, output_file=args.output)
