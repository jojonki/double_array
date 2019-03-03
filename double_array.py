import os

class DoubleArray:
    def __init__(self, code, data_size=10):
        self.__base = [0] * data_size
        self.__check = [0] * data_size
        self.__code = code
        # ['ab#']
        # self.__base  = [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        # self.__check = [0, 0, 1, 2, 0, 0, 0, 3, 0, 0, 0]

        # ['ab#', 'abc#']
        # self.__base  = [0, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0]
        # self.__check = [0, 0, 1, 2, 3, 0, 0, 3, 4, 0, 0]
        self.__data_size = data_size
        
    @property
    def code(self):
        return self.__code

    @property
    def base(self):
        return self.__base

    @property
    def check(self):
        return self.__check

    @property
    def N(self):
        return self.__data_size

    def report(self):
        print('i:  {}'.format(', '.join([str(i) for i in range(1, self.N)])))
        print('b: {}'.format(self.base[1:]))
        print('c: {}'.format(self.check[1:]))

    def search(self, word):
        """Search a word in the double array

        Rerutns:
            Return the search result with information
            (found: boolean, final_node: int, final_chara: str)
        """
        if not word or type(word) != str: # unsafe return values
            return False, None, None

        s = 1 # start node
        for c_ind, c in enumerate(word):
            next_node = self.base[s] + self.code[c]
            if self.check[next_node] == s:
                # check ok. move to:', next_node
                s = next_node
            else:
                # 'search fail at `c` in `word`
                return False, s, c

        return True, None, None

    def _registerVocab(self, s, c):
        """
        """
        if self.base[s] == 0: # Not used based node
            # Search empty check node
            for ind in range(1 + self.code[c], self.N):
                if self.check[ind] == 0:
                    self.base[s] = ind - self.code[c]
                    self.check[ind] = s
                    break
            # TODO Handle if theare are no empty check
        else: # Used base node
            if self.check[self.base[s] + self.code[c]] == 0: # if there is an availabe check
                self.check[self.base[s] + self.code[c]] = s
            else: # node conflicted
                # Re-assign base and check nodes
                # Gather all children nodes whose parent is the conflict node
                child_node_list = [ch_i for ch_i, ch_v in enumerate(self.check) if ch_v == s]
                # Gather all children values whose parent is the conflict node
                child_code_list = [ch_n - self.base[s] for ch_n in child_node_list]
                # The parent of the new adding node will be the conflict node
                child_code_list += [self.code[c]] # also add the char of the new vocab
                # Search new empty check for the children
                for i in range(1, self.N):
                    # Check availability of check for the children
                    if sum([self.check[i + code_v] for code_v in child_code_list]) == 0:
                        offset = i
                        org_base = self.base[s] # save the old offset
                        self.base[s] = offset
                        # Update the node and check of the all children with the new offset
                        for node in child_node_list:
                            code_v = node - org_base
                            prev_dst_node = org_base + code_v
                            new_dst_node = offset + code_v
                            self.base[new_dst_node] = self.base[prev_dst_node]
                            self.check[new_dst_node] = s

                            # Update children whose parent is the updated node, i.e., the grand parent is the conflict node
                            for j in range(1, self.N):
                                if self.check[j] == prev_dst_node:
                                    self.check[j] = new_dst_node

                            # Clear old information of the child
                            self.base[prev_dst_node] = 0
                            self.check[prev_dst_node] = 0

                        # Set check for the new character
                        self.check[offset + self.code[c]] = s
                        self.report()
                        break
                # TODO handle if there are no empty check

    def _build(self, vocab):
        ret, s, c = self.search(vocab) # bool, final_node, final_char
        if ret:
            print('success')
        else:
            self._registerVocab(s, c)
            self._build(vocab) # TODO(jonki) recursive call should be handled safely

    def build(self, vocab_list):
        """Build an double array from a vocabulary list

        Args:
            vocab_list: An array of vocabuary(str)

        Returns:
            A boolean indicating if it succeed to build the dictioanry or not.
        """
        for vocab in vocab_list:
            print('vocab', vocab)
            self._build(vocab)

    def commonPrefixSearch(self, input_str):
        """Search all common prefix from the dictionary

        Args:
            input_str: A sentence of the query.

        Return:
            prefix_list: A list of words contains input_str as prefix
        """
        pass

    def save(self, fpath, base, check):
        """Save a double array to a file"""
        with open(fpath, 'w') as fout:
            fout.write('{}\n'.format(','.join(base)))
            fout.write('{}\n'.format(','.join(check)))

    def load(self, fpath):
        """Load a file of a double array"""
        ret = False
        if os.path.exists(fpath):
            with open(fpath, 'r') as fin:
                lines = fin.readlines()
                if len(lines) == 2:
                    self.base = lines[0]
                    self.check = lines[1]
                    ret = True
                else:
                    print('Invalid double array format')
        else:
            print('{} does not exist'.format(fpath))

        return ret
