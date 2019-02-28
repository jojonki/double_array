import sys

terminated_char = '#'
chars = ['a', 'b', 'c', 'd', 'e', '#']
code = {char: i+1 for i, char in enumerate(chars)}
v2c = {v:i for i, v in code.items()}
print('code', code)

class DoubleArray:
    def __init__(self, data_size=10):
        self.__base = [0] * data_size
        self.__check = [0] * data_size
        # ['ab#']
        # self.__base  = [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        # self.__check = [0, 0, 1, 2, 0, 0, 0, 3, 0, 0, 0]

        # ['ab#', 'abc#']
        # self.__base  = [0, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0]
        # self.__check = [0, 0, 1, 2, 3, 0, 0, 3, 4, 0, 0]
        self.__data_size = data_size
        
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
        if not word or type(word) != str:
            return False, None

        s = 1 # start node
        for c_ind, c in enumerate(word):
            print('search', c, ', current', s)
            next_node = self.base[s] + code[c]
            if self.check[next_node] == s:
                print('check ok. move to:', next_node)
                s = next_node
            else:
                print('search fail at', c, 'in', word)
                return False, s, c

        return True, None, None


    def _build(self, vocab):
        ret, s, c = self.search(vocab) # bool, final_node, final_char
        if ret:
            print('success')
        else:
            if self.base[s] == 0: # not registered
                for ind in range(1 + code[c], self.N):
                    if self.check[ind] == 0:
                        self.base[s] = ind - code[c]
                        self.check[ind] = s
                        break
            else:
                if self.check[self.base[s] + code[c]] == 0:
                    self.check[self.base[s] + code[c]] = s
                else:
                    # 衝突発生ノードを親に持つノードのindexを取得
                    child_node_list = [ch_i for ch_i, ch_v in enumerate(self.check) if ch_v == s]
                    # 衝突発生ノードを親に持つノードのコード値を取得
                    child_code_list = [ch_n - self.base[s] for ch_n in child_node_list]
                    # 新たに追加しようとしている文字コード値も子ノードになるため追加
                    child_code_list += [code[c]] # also add the char of the new vocab
                    # 子ノードが利用できる空のcheck要素を探す
                    for i in range(1, self.N):
                        if sum([self.check[i + code_v] for code_v in child_code_list]) == 0:
                            x = i
                            org_base = self.base[s]
                            self.base[s] = x
                            # Update check of the children
                            # for code_v in child_code_list:
                            #     self.check[x + v2c[code_v]] = s
                                # copy new base for the new destination
                            for node in child_node_list:
                                code_v = node - org_base
                                prev_dst_node = org_base + code_v
                                new_dst_node = x + code_v
                                self.base[new_dst_node] = self.base[prev_dst_node]
                                self.check[new_dst_node] = s

                                # 元遷移先のノードを親とするノード一覧のcheckも更新
                                for j in range(1, self.N):
                                    if self.check[j] == prev_dst_node:
                                        self.check[j] = new_dst_node

                                # 元遷移先をクリア
                                self.base[prev_dst_node] = 0
                                self.check[prev_dst_node] = 0
                            # 新しく追加する文字コード値のノードのcheckもセット
                            self.check[x + code[c]] = s
                            self.report()
                            break
            self._build(vocab)

    def build(self, vocab_list):
        for vocab in vocab_list:
            print('vocab', vocab)
            self._build(vocab)

    def commonPrefixSearch(self):
        pass


def main():
    vocab_list = ['ab#', 'abc#']
    vocab_list = ['ab#', 'abc#', 'ac#']
    # vocab_list = ['abc#']
    # vocab_list = ['ac#']
    da = DoubleArray()
    print('INIT-----------------')
    da.report()
    print('---------------------')
    da.build(vocab_list)
    print('FINAL----------------')
    da.report()


if __name__ == '__main__':
    main()
