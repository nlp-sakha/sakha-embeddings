import argparse

from parser_edersaas import parser as edersaas_parser
from parser_kyym import parser as kyym_parser
from parser_sakhasire import parser as sakhasire_parser
from parser_sakhalife_sahalii import parser as sakhalife_parser
from parser_iltymen import parser as iltymen_parser


def main(newspaper_name, output, from_page=0, to_page=10):
    if output is None:
        assert (ValueError('need to specify output file'))
    current_parser = None
    if newspaper_name == 'kyym':
        current_parser = kyym_parser
    elif newspaper_name == 'edersaas':
        current_parser = edersaas_parser
    elif newspaper_name == 'sakhasire':
        current_parser = sakhasire_parser
    elif newspaper_name == 'sakhalife_sahalii':
        current_parser = sakhalife_parser
    elif newspaper_name == 'iltymen':
        current_parser = iltymen_parser
    else:
        assert (ValueError('newspaper_name is not known'))
    print_each = (to_page - from_page) // 10
    parsed = current_parser(from_page, to_page, output=output, print_each=print_each)
    print('RESULT: {} articles parsed from {}'.format(parsed, newspaper_name))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Utilit for parsing some websites '
                                                    'with sakha language content')
    argparser.add_argument('newspaper_name',
                           action='store',
                           type=str,
                           choices=['kyym', 'edersaas', 'sakhasire', 'sakhalife_sahalii', 'iltymen'],
                           help='"kyym", "edersaas", "iltymen", "sakhalife_sahalii" or "sakhasire". Example: python kyym ...')
    argparser.add_argument('-f',
                           '--from_page',
                           type=int,
                           help='Number of article from which we are starting to parse',
                           default=0)
    argparser.add_argument('-t',
                           '--to_page',
                           type=int,
                           help='Number of final article which we are parsing',
                           default=1)
    argparser.add_argument('-o',
                           '--output',
                           type=str,
                           help='Address to file where data will be placed.',
                           default='parser_output.txt')

    args = argparser.parse_args()

    main(newspaper_name=args.newspaper_name,
         from_page=args.from_page,
         to_page=args.to_page,
         output=args.output)
#python3 parser/parser.py sakhalife_sahalii -f 0 -t 2000 -o data/corpus.sakhalife.txt
#python3 parser/parser.py kyym -f 0 -t 50 -o data/corpus.kyym.txt
