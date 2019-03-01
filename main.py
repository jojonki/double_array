import os
import sys

from double_array import DoubleArray


def main():
    # terminated_char = '#'
    chars = ['a', 'b', 'c', 'd', 'e', '#']
    code = {char: i+1 for i, char in enumerate(chars)}
    v2c = {v:i for i, v in code.items()}
    print('code', code)

    # vocab_list = ['ab#', 'abc#']
    vocab_list = ['ab#', 'abc#', 'ac#']
    # vocab_list = ['abc#']
    # vocab_list = ['ac#']
    da = DoubleArray(code)
    print('INIT-----------------')
    da.report()
    print('---------------------')
    da.build(vocab_list)
    print('FINAL----------------')
    da.report()


if __name__ == '__main__':
    main()
