import unittest
from double_array import DoubleArray


class TesDoubleArray(unittest.TestCase):
    def setUp(self):
        chars = ['a', 'b', 'c', 'd', 'e', '#']
        self.code = {char: i+1 for i, char in enumerate(chars)}
        self.v2c = {v:i for i, v in self.code.items()}
        self.da = DoubleArray(self.code)

    def test_doubleArray(self):
        exp_base  = [0, 1, 3, 0, 2, 1, 3, 0, 0, 0]
        exp_check = [0, 0, 1, 0, 5, 2, 2, 5, 4, 6]
        vocab_list = ['ab', 'abc', 'ac']
        self.da.build(vocab_list)
        self.assertEqual(exp_base, self.da.base[:len(exp_base)])
        self.assertEqual(exp_check, self.da.check[:len(exp_base)])

    def test_commonPrefixSearch(self):
        self.da.clear()
        vocab_list = ['ab', 'abc', 'ac']
        self.da.build(vocab_list)

        sent1 = 'aca'
        sent2 = 'abcd'
        cp_list = self.da.commonPrefixSearch(sent1)
        self.assertEqual(['ac'], cp_list)
        cp_list = self.da.commonPrefixSearch(sent2)
        self.assertEqual(['ab', 'abc'], cp_list)

if __name__ == "__main__":
    unittest.main()
