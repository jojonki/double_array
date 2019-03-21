import argparse
import gzip
import os
import sys
from tqdm import tqdm

from double_array import DoubleArray

def build(da, vocab_file):
    with open(vocab_file, 'r') as f:
        word_list = sorted([l.rstrip() for l in f.readlines()])
    word_list = [w + '#' for w in word_list if not w.startswith('#')]
    print('word_list', word_list[:10])

    print('Building vocabuary...')
    da.build(word_list)
    print('Built!')
    da.save('./models/dict')
    da.report()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vocab', type=str, metavar='PATH', required=True, help='vocabulary file')
    parser.add_argument('--dict', type=str, metavar='PATH', help='build double array')
    args = parser.parse_args()

    da = DoubleArray()
    if args.dict:
        da.load(args.dict)
    else:
        build(da, args.vocab)
        # da.report(verbose=True)


    query_list = ['東', '東京', '東京タワー', '東京都議会', '加藤清正']
    for q in query_list:
        print('=====Search {}======'.format(q))
        cp_list = da.commonPrefixSearch(q)
        print('commonPrefixSearch("{}"): {}'.format(q, cp_list))


if __name__ == '__main__':
    main()
