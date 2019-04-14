# double_array

## My environment
- python 3.6.1
- cython 0.25.2
- tqdm


## Set up
1. Generate a vocabulary file ipadic data.
- Download IPA dictionary (mecab-ipadic-2.7.0-20070801.tar.gz) from [here](https://taku910.github.io/mecab/)
- tar zxvf mecab-ipadic-2.7.0-20070801.tar.gz && mv mecab-ipadic-2.7.0-20070801 ./utils/
- Generate a vocabulary file from the dictionary.
    ```
    $ python utils/gen_vocabs_from_mecab_ipadic.py
    -> ./utils/ipadic-vocab.txt will be created.
    ```

2. Build your double-array from the vocabulary file.
- It may needs a few minutes. (two minutes with my MacBook Pro 2017).
```
$ ./build_and_run.sh
```

## Usages
### Common Prefix Search
```
$ python main.py --dict models/ipadic-vocab.txt.dict --cpq すもも,東京
=====Search すもも======
"す" found in the dictionary
"すも" found in the dictionary
"すもも" found in the dictionary
commonPrefixSearch("すもも"): ['す', 'すも', 'すもも']
=====Search 東京======
"東" found in the dictionary
"東京" found in the dictionary
commonPrefixSearch("東京"): ['東', '東京']
Process time: 0.5s
```

### Common Prefix Search
```
$ python examples/common_prefix_search.py --dict models/ipadic-vocab.txt.dict --q すもも,吾輩
=====Search すもも======
"す" found in the dictionary
"すも" found in the dictionary
"すもも" found in the dictionary
commonPrefixSearch("すもも"): ['す', 'すも', 'すもも']
=====Search 吾輩======
"吾" found in the dictionary
"吾輩" found in the dictionary
commonPrefixSearch("吾輩"): ['吾', '吾輩']
Process time: 0.5s
```

### Longest Match Tokenization
```
$ python examples/longest_match.py --dict models/ipadic-vocab.txt.dict --q 吾輩は猫である   [~/git/double_array]
Input: 吾輩は猫である
"吾" found in the dictionary
"吾輩" found in the dictionary
"吾輩は" NOT found in the dictionary
"吾輩は猫" NOT found in the dictionary
"吾輩は猫で" NOT found in the dictionary
"吾輩は猫であ" NOT found in the dictionary
"吾輩は猫である" NOT found in the dictionary
"は" found in the dictionary
"は猫" NOT found in the dictionary
"は猫で" NOT found in the dictionary
"は猫であ" NOT found in the dictionary
"は猫である" NOT found in the dictionary
"猫" found in the dictionary
"猫で" NOT found in the dictionary
"猫であ" NOT found in the dictionary
"猫である" NOT found in the dictionary
"で" found in the dictionary
"であ" NOT found in the dictionary
"である" NOT found in the dictionary
"あ" found in the dictionary
"ある" found in the dictionary
Result: ['吾輩', 'は', '猫', 'で', 'ある']
Process time: 0.6s
```

## TODOs
- [ ] add tests
