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

3. Run common prefix search with the double-array.
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

## TODOs
- [ ] add tests
