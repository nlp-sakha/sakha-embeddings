if [ ! -f ./data/all.txt ]; then
    if [ ! -f ./data/sahwiki-latest-pages-articles.xml.bz2 ]; then
        wget -P data/ https://dumps.wikimedia.org/sahwiki/latest/sahwiki-latest-pages-articles.xml.bz2
    fi
    python parser/wikitodata.py data/sahwiki-latest-pages-articles.xml.bz2  data/wiki.txt
    python parser/parser.py kyym -f 0 -t 2000 -o data/corpus.kyym.txt
    python parser/parser.py edersaas -f 0 -t 100 -o data/corpus.edersaas.txt
    python parser/parser.py sakhasire -f 0 -t 100 -o data/corpus.sakhasire.txt
    python parser/parser.py sakhalife_sahalii -f 0 -t 2000 -o data/corpus.sakhalife.txt
    python parser/parser.py iltymen -f 0 -t 2000 -o data/corpus.iltymen.txt
    python parser/parser.py ysia -f 0 -t 2000 -o data/corpus.ysia.txt
    cat data/wiki.txt >> data/all.txt
    cat data/corpus.kyym.txt >> data/all.txt
    cat data/corpus.edersaas.txt >> data/all.txt
    cat data/corpus.sakhasire.txt >> data/all.txt
fi
