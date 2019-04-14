#!/bin/sh

python setup.py build_ext --inplace

python main.py --vocab ./ipadic-vocab.txt
