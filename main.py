import gzip
import os
import sys
from tqdm import tqdm

from double_array import DoubleArray


def main():
    # vocab_list = ['ab#', 'abc#']
    with open('data/simple_words.txt', 'r') as f:
        word_list = sorted([l.rstrip() for l in f.readlines()])
    word_list = [w for w in word_list if not w.startswith('#')]
    word_list += ['#']
    print('word_list', word_list)
    # word_list = ['a', 'ab', 'abc', 'ac', 'd', '#']
    # vocab_list = ['abc#']
    # vocab_list = ['ac#']

    vocab_list = []
    for word in tqdm(word_list):
        for c in word:
            if c not in vocab_list:
                vocab_list.append(c)
    vocab_list = sorted(vocab_list)
    print('vocab_list', vocab_list)
    
    # terminated_char = '#'
    # chars = ['a', 'b', 'c', 'd', 'e', '#']
    code = {char: i+1 for i, char in enumerate(vocab_list)}
    v2c = {v:i for i, v in code.items()}
    print('code', code)

    da = DoubleArray(code, data_size=40)
    print('INIT-----------------')
    # da.report()
    print('---------------------')
    da.build(word_list)
    print('FINAL----------------')
    # da.report()

    print('Test')
    query_list = ['東', '東京', '東京タワー', '東京都議会']
    for q in query_list:
        print('=====Search {}======'.format(q))
        cp_list = da.commonPrefixSearch(q)
        print('commonPrefixSearch("{}"): {}'.format(q, cp_list))



if __name__ == '__main__':
    main()
