import sys

terminated_char = '#'
chars = ['a', 'b', 'c', 'd', 'e', '#']
code = {char: i+1 for i, char in enumerate(chars)}
print('code', code)

class DoubleArray:
    def __init__(self, data_size=10):
        # self.__base = [0] * data_size
        # self.__check = [0] * data_size
        # ['ab#']
        self.__base  = [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        self.__check = [0, 0, 1, 2, 0, 0, 0, 3, 0, 0, 0]
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
                print('search fail', word[:c_ind+1])
                return False, s

        return True, None


    def build(self, vocab_list):
        self.report()
        for vocab in vocab_list:
            print('vocab', vocab)
            
            ret, final_node = self.search(vocab)
            if ret:
                print('success')
            else:
                print('fail', final_node)
                s = final_node # start registaration

                for c_ind, c in enumerate(vocab[s-1:]):
                    x = None
                    for ind in range(1 + code[c], self.N):
                        if self.check[ind] == 0:
                            x = (ind - code[c])
                            break

                    if x is not None:
                        self.base[s] = x
                        next_node = x + code[c]
                        self.check[next_node] = s
                        s = next_node
                    else:
                        print('cannot find an empty check element')
                        sys.exit()

            continue

            s = 1 # start node
            for v_ind, c in enumerate(vocab):
                x = None
                for ind in range(1 + code[c], self.N):
                    if self.check[ind] == 0:
                        x = (ind - code[c])
                        break
                if x is not None:
                    self.base[s] = x # set offset
                    next_node = x + code[c]
                    print('check[{}]={}'.format(next_node, self.check[next_node]))
                    self.check[next_node] = s # set parent node
                    s = next_node # move to next node
                    print('insert', c)
                    print('i:  {}'.format(', '.join([str(i) for i in range(1, self.N)])))
                    print('b: {}'.format(self.base[1:]))
                    print('c: {}'.format(self.check[1:]))
                else:
                    print('cannot find an empty check element')
                    sys.exit()
            print()


    def commonPrefixSearch(self):
        pass


def main():
    vocab_list = ['ab#', 'abc#']
    da = DoubleArray()
    da.build(vocab_list)
    print('----------------')
    da.report()


if __name__ == '__main__':
    main()
