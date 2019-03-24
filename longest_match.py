"""Longest match search sample"""

import argparse
import codecs
import glob
import gzip
import os
import sys
import time
from tqdm import tqdm

from double_array import DoubleArray


def longest_search(da, query):
    print('Input:', query)
    begin = 0
    end = len(query)
    result = []
    while begin < end:
        cp_list = da.commonPrefixSearch(query[begin:])
        longest = max(cp_list, key=len)
        result.append(longest)
        begin += len(longest)

    print('Result:', result)


def main():
    begin_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--dict', type=str, metavar='PATH', help='build double array')
    # parser.add_argument('--cpq', type=str, help='query of commonPrefixSearch. Use commna (,) to specify multi queries.')
    args = parser.parse_args()

    da = DoubleArray()
    da.load(args.dict)


    query = '行き当りばったりみごと素敵'
    longest_search(da, query)

    print('Process time: {:.1f}s'.format(time.time() - begin_time))


if __name__ == '__main__':
    main()
