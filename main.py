import gzip
import os
import sys
from tqdm import tqdm

from double_array import DoubleArray


def main():
    # with open('data/simple_words.txt', 'r') as f:
    with open('data/words.txt', 'r') as f:
        word_list = sorted([l.rstrip() for l in f.readlines()])
    word_list = [w + '#' for w in word_list if not w.startswith('#')]
    print('word_list', word_list[:10])

    da = DoubleArray()
    print('INIT-----------------')
    da.report()
    print('---------------------')
    da.build(word_list)
    print('FINAL----------------')
    da.report()

    print('Test')
    query_list = ['東', '東京', '東京タワー', '東京都議会', '加藤清正']
    for q in query_list:
        print('=====Search {}======'.format(q))
        cp_list = da.commonPrefixSearch(q)
        print('commonPrefixSearch("{}"): {}'.format(q, cp_list))



if __name__ == '__main__':
    main()
