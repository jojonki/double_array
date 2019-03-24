import os
import sys
from tqdm import tqdm

T = '#'

class DoubleArray:
    def __init__(self, data_size=20):
        self._data_size = data_size
        self._base = []
        self._check = []
        self.clear()
        
    @property
    def base(self):
        return self._base

    @property
    def check(self):
        return self._check

    @property
    def N(self):
        assert len(self._base) == len(self._check)
        return len(self._base)

    def _expand(self, diff):
        """Expand double array"""
        if diff > 0:
            self._base += [0] * diff
            self._check += [0] * diff

    def clear(self):
        self._base = [0] * self._data_size
        self._check = [0] * self._data_size

    def report(self, verbose=False):
        print('Array length: {}'.format(self.N))
        d_size = (sys.getsizeof(self._base) + sys.getsizeof(self._check))
        unit = 'B'
        if d_size > 1024:
            unit = 'KB'
            d_size /= 1024
        if d_size > 1024:
            unit = 'MB'
            d_size /= 1024
        print('Double-Array size: {:.1f} {}'.format(d_size, unit))
        if verbose:
            print('i:  {}'.format(', '.join([str(i) for i in range(1, self.N)])))
            print('b: {}'.format(self.base[1:]))
            print('c: {}'.format(self.check[1:]))

    def search(self, word, start_node=1):
        """Search a word in the double array

        Rerutns:
            Return the search result with information
            (found: boolean, final_node: int, final_chara: str)
        """
        crnt_node = start_node
        crnt_char = None
        for c_ind, c in enumerate(word):
            next_node = self.base[crnt_node] + c
            if next_node < len(self.check) and self.check[next_node] == crnt_node:
                # check ok. move to:', next_node
                crnt_node = next_node
                crnt_char = c
            else:
                # 'search fail at `c` in `word`
                return False, crnt_node, c

        return True, crnt_node, crnt_char

    def _registerVocab(self, s, c):
        """
        """
        if self.base[s] == 0: # Not used based node
            # Search an empty check node
            try:
                dst_check_index = 1 + c + self._check[1+c:].index(0)
            except ValueError as e: # No empty check nodes
                # Expand check
                self._expand(1)
                dst_check_index = self.N - 1

            self.base[s] = dst_check_index - c
            self.check[dst_check_index] = s
        else: # Used base node
            if (self.base[s] + c < self.N) and self.check[self.base[s] + c] == 0: # if check is correct
                self.check[self.base[s] + c] = s
            else: # node conflicted
                # Re-assign base and check nodes
                # Gather all children nodes whose parent is the conflict node
                child_node_list = [ch_i for ch_i, ch_v in enumerate(self.check) if ch_v == s]
                # Gather all children values whose parent is the conflict node
                # The parent of the new adding node will be the conflict node
                child_code_list = [ch_n - self.base[s] for ch_n in child_node_list] + [c]
                # child_code_list += [c] # also add the char of the new vocab
                # max_ind = max(self.N + code_v + 1 for code_v in child_code_list)
                # self._expand(max_ind - len(self._check)) # TODO maybe wrong
                for i in range(1, self.N):
                    # Search new empty check for the children
                    found_empty_check = True

                    # Check available check for all the children
                    max_ind = i + child_code_list[-1] + 1 # last child_code is the largest.
                    self._expand(max_ind - len(self._check)) # TODO maybe wrong

                    # All check must be 0
                    for code_v in child_code_list:
                        if self.check[i + code_v] != 0:
                            found_empty_check = False
                            break

                    if not found_empty_check: # Found available check
                        continue

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
                    self.check[offset + c] = s
                    # self.report()
                    break
                # TODO handle if there are no empty check
                if not found_empty_check:
                    sys.exit('Could not find empty check when it conflicts')

    def _build(self, vocab):
        if type(vocab) == str:
            vocab = vocab.encode('utf-8')
        ret, s, c = self.search(vocab) # bool, final_node, final_char
        if ret:
            print(vocab.decode('utf-8'), 'in the dic')
        else:
            # print(vocab.decode('utf-8'), 'NOT in the dic. Add', vocab.decode('utf-8'))
            self._registerVocab(s, c)
            if c != 35: # 35 == '#'
                self._build(vocab) # TODO(jonki) recursive call should be handled safely

    def build(self, vocab_list):
        """Build an double array from a vocabulary list.

        Args:
            vocab_list: An array of vocabuary(str)

        Returns:
            A boolean indicating if it succeed to build the dictioanry or not.
        """
        for vocab in tqdm(vocab_list):
            print('Build vocab:', vocab)
            if not vocab.endswith(T):
                vocab += T
            self._build(vocab)
            self.report()

    def commonPrefixSearch(self, input_str):
        """Search all common prefix of input string from the dictionary.

        Args:
            input_str: A sentence of the query.

        Return:
            prefix_list: A list of words contains input_str as prefix
        """
        cp_list = []
        final_node = 1
        for ind, char in enumerate(input_str, 1):
            byte_char = char.encode('utf-8')
            ret, final_node, final_char = self.search(byte_char, start_node=final_node)
            # if ret and self.check[self.base[final_node] + T] == final_node:
            if ret and self.check[self.base[final_node] + 35] == final_node: # '#' -> 35
                print('"{}" found in the dictionary'.format(input_str[:ind]))
                cp_list.append(input_str[:ind])
            else:
                print('"{}" NOT found in the dictionary'.format(input_str[:ind]))

        return cp_list


    def save(self, fpath):
        """Save a double array to a file"""
        with open(fpath, 'w') as fout:
            fout.write('{}\n'.format(','.join([str(ind) for ind in self.base])))
            fout.write('{}\n'.format(','.join([str(ind) for ind in self.check])))

    def load(self, fpath):
        """Load a file of a double array"""
        ret = False
        if os.path.exists(fpath):
            with open(fpath, 'r') as fin:
                lines = fin.readlines()
                if len(lines) == 2:
                    self._base  = [int(ind) for ind in lines[0].split(',')]
                    self._check = [int(ind) for ind in lines[1].split(',')]
                    ret = True
                else:
                    print('Invalid double array format')
        else:
            print('{} does not exist'.format(fpath))

        return ret
