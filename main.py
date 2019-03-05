import os
import sys

from double_array import DoubleArray


def main():
    # vocab_list = ['ab#', 'abc#']
    word_list = ['a', 'ab', 'abc', 'ac', 'd', '#']
    # vocab_list = ['abc#']
    # vocab_list = ['ac#']

    vocab_list = []
    for word in word_list:
        for c in word:
            if c not in vocab_list:
                vocab_list.append(c)
    vocab_list = sorted(vocab_list)
    
    # terminated_char = '#'
    # chars = ['a', 'b', 'c', 'd', 'e', '#']
    code = {char: i+1 for i, char in enumerate(vocab_list)}
    v2c = {v:i for i, v in code.items()}
    print('code', code)

    da = DoubleArray(code)
    print('INIT-----------------')
    da.report()
    print('---------------------')
    da.build(word_list)
    print('FINAL----------------')
    da.report()

    sent = 'abcd'
    cp_list = da.commonPrefixSearch(sent)
    print('commonPrefixSearch("{}"): {}'.format(sent, cp_list))



if __name__ == '__main__':
    main()
