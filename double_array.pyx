import os
import sys
from tqdm import tqdm
import cython

T = '#'

cdef class DoubleArray:
    cdef public int _data_size
    cdef public list _base
    cdef public list _check
    cdef public int _left
    def __init__(self, data_size=20):
        self._data_size = data_size
        self._base = []
        self._check = []
        self.clear()

        self._left = 1

    cdef _expand(self, int diff):
        """Expand double array"""
        if diff > 0:
            self._base += [0] * diff
            self._check += [0] * diff

    def clear(self):
        self._base = [0] * self._data_size
        self._check = [0] * self._data_size

    def report(self, verbose=False):
        N = len(self._base)
        print('Array length: {}'.format(N))
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
            print('i:  {}'.format(', '.join([str(i) for i in range(1, N)])))
            print('b: {}'.format(self._base[1:]))
            print('c: {}'.format(self._check[1:]))

    cdef search(self, bytes word, int start_node=1):
        """Search a word in the double array

        Rerutns:
            Return the search result with information
            (found: boolean, final_node: int, final_chara: str)
        """
        crnt_node = start_node
        crnt_char = None
        for c_ind, c in enumerate(word):
            next_node = self._base[crnt_node] + c
            if next_node < len(self._check) and self._check[next_node] == crnt_node:
                # check ok. move to:', next_node
                crnt_node = next_node
                crnt_char = c
            else:
                # 'search fail at `c` in `word`
                return False, crnt_node, c, c_ind

        return True, crnt_node, crnt_char, c_ind

    cdef refreshCheck(self, int prev_dst_node, int new_dst_node):
        res = []
        for j in range(1, len(self._base)):
            if self._check[j] == prev_dst_node:
                self._check[j] = new_dst_node
                res.append(j)
        print('########')
        print(res)
        print(prev_dst_node, new_dst_node)

    cdef _registerVocab(self, bytes vocab, int s):
        for c in vocab:
            if self._base[s] == 0: # Not used based node
                # Search an empty check node
                try:
                    check_idx = 1 + c + self._check[1+c:].index(0)
                except ValueError as e: # No empty check nodes
                    # Expand check
                    self._expand(1)
                    check_idx = len(self._base) - 1

                self._base[s] = check_idx - c
                self._check[check_idx] = s
                s = check_idx # move to next node
            else: # Used base node
                # N = len(self._base)
                if (self._base[s] + c < len(self._base)) and self._check[self._base[s] + c] == 0: # if check is correct
                    self._check[self._base[s] + c] = s
                    s = self._base[s] + c # move to next node
                else: # node conflicted
                    # Re-assign base and check nodes
                    # Gather all children nodes whose parent is the conflict node
                    # Gather all children values whose parent is the conflict node
                    # The parent of the new adding node will be the conflict node
                    # child_node_list, child_code_list = [], []
                    # for ch_i, ch_v in enumerate(self._check):
                    #     if ch_v == s:
                    #         child_node_list.append(ch_i)
                    #         child_code_list.append(ch_i - self._base[s])
                    offset = self._base[s]
                    # child_node_list = [ch_i for ch_i, ch_v in enumerate(self._check) if ch_v == s]
                    # child_code_list = [ch_i - offset for ch_i in child_node_list] + [c]

                    # beg = s + offset
                    # end = beg + 255
                    beg = max(0, min(s, offset) - 255)
                    end = min(len(self._base), max(s, offset) + 255)
                    child_node_list2 = [ch_i + beg for ch_i, ch_v in enumerate(self._check[beg:end]) if ch_v == s]
                    child_code_list2 = [ch_i - offset for ch_i in child_node_list2] + [c]
                    # print('----------------')
                    # print(child_node_list)
                    # print(child_node_list2)
                    # assert len(child_node_list) == len(child_node_list2)
                    # for a1, a2 in zip(child_node_list, child_node_list2):
                    #     assert a1 == a2



                    for i in range(self._left, len(self._base)):
                        # Search new empty check for the children
                        found_empty_check = True

                        # Check available check for all the children
                        # max_ind = i + child_code_list[-1] + 1 # last child_code is the largest.
                        max_ind = i + c + 1 # last child_code is the largest. TODO really correct?
                        self._expand(max_ind - len(self._check)) # TODO maybe wrong

                        # All check must be 0
                        for code_v in child_code_list2:
                            if self._check[i + code_v] != 0:
                                found_empty_check = False
                                break

                        if not found_empty_check: # Found available check
                            continue

                        # FOUND an empty node
                        if self._check[self._left:i].count(0) < (i - self._left + 1) * 0.05:
                            self._left = i

                        offset = i
                        org_base = self._base[s] # save the old offset
                        self._base[s] = offset
                        # Update the node and check of the all children with the new offset
                        for node in child_node_list2:
                            code_v = node - org_base
                            prev_dst_node = org_base + code_v
                            new_dst_node = offset + code_v
                            self._base[new_dst_node] = self._base[prev_dst_node]
                            self._check[new_dst_node] = s

                            # Update children whose parent is the updated node, i.e., the grand parent is the conflict node
                            # TODO サイズが大きくなるほどここは遅い
                            # self.refreshCheck(prev_dst_node, new_dst_node)
                            res = []
                            try:
                                min_j = self._check.index(prev_dst_node)
                                # for j in range(1, len(self._base)): hoge
                                for j in range(min_j, min(len(self._base), min_j+255)):
                                    # for j in range(org_base, prev_dst_node):
                                    if self._check[j] == prev_dst_node:
                                        self._check[j] = new_dst_node
                                        res.append(j)
                                # if res:
                                #     print(res, max(res) - min(res) < 255)
                            except ValueError as e: # No empty check nodes
                                pass

                            # Clear old information of the child
                            self._base[prev_dst_node] = 0
                            self._check[prev_dst_node] = 0

                        # Set check for the new character
                        self._check[offset + c] = s
                        # self.report()
                        s = offset + c # move to next node
                        break
                    # TODO handle if there are no empty check
                    if not found_empty_check:
                        sys.exit('Could not find empty check when it conflicts')

    cdef _build(self, bytes vocab):
        ret, s, c, char_ind = self.search(vocab) # bool, final_node, final_char
        if ret:
            pass
            # print(vocab.decode('utf-8'), 'in the dic')
        else:
            self._registerVocab(vocab[char_ind:], s)

    cpdef build(self, list vocab_list):
        """Build an double array from a vocabulary list.

        Args:
            vocab_list: An array of vocabuary(str)

        Returns:
            A boolean indicating if it succeed to build the dictioanry or not.
        """
        for vocab in tqdm(vocab_list):
            # print('Build vocab:', vocab)
            if not vocab.endswith(T):
                vocab += T
            self._build(vocab.encode('utf-8'))
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
            ret, final_node, final_char, char_ind = self.search(byte_char, start_node=final_node)
            # if ret and self._check[self._base[final_node] + T] == final_node:
            if ret and self._check[self._base[final_node] + 35] == final_node: # '#' -> 35
                print('"{}" found in the dictionary'.format(input_str[:ind]))
                cp_list.append(input_str[:ind])
            else:
                print('"{}" NOT found in the dictionary'.format(input_str[:ind]))

        return cp_list


    def save(self, fpath):
        """Save a double array to a file"""
        with open(fpath, 'w') as fout:
            fout.write('{}\n'.format(','.join([str(ind) for ind in self._base])))
            fout.write('{}\n'.format(','.join([str(ind) for ind in self._check])))

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
