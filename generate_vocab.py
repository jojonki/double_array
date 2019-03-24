"""Generate a vocabulary file from ipadic"""

import argparse
import codecs
import glob
import os
import time


def main():
    begin_time = time.time()

    parser = argparse.ArgumentParser()
    # parser.add_argument('--vocab', type=str, metavar='PATH', help='vocabulary file')
    # parser.add_argument('--dict', type=str, metavar='PATH', help='build double array')
    # parser.add_argument('--cpq', type=str, help='query of commonPrefixSearch. Use commna (,) to specify multi queries.')
    args = parser.parse_args()

    # get all the csv files in that directory (assuming they have the extension .csv)
    ipadic_dir = './mecab-ipadic-2.7.0-20070801'
    csv_files = glob.glob(os.path.join(ipadic_dir, '*.csv'))
    with open('ipadic-vocab.txt', 'w') as fout:
        for c in csv_files:
            print('Load', c)
            with codecs.open(c, 'r', 'euc_jp') as fin:
                for l in fin:
                    fout.write('{}\n'.format(l.split(',')[0]))



    print('Process time: {:.1f}s'.format(time.time() - begin_time))


if __name__ == '__main__':
    main()
