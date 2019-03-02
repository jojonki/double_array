import unittest
from double_array import DoubleArray


class TesDoubleArray(unittest.TestCase):
    def setUp(self):
        chars = ['a', 'b', 'c', 'd', 'e', '#']
        self.code = {char: i+1 for i, char in enumerate(chars)}
        self.v2c = {v:i for i, v in self.code.items()}
        self.da = DoubleArray(self.code)

    def test_tashizan(self):
        exp_base  = [0, 1, 3, 0, 2, 1, 3, 0, 0, 0]
        exp_check = [0, 0, 1, 0, 5, 2, 2, 5, 4, 6]
        vocab_list = ['ab#', 'abc#', 'ac#']
        self.da.build(vocab_list)
        self.assertEqual(exp_base, self.da.base)
        self.assertEqual(exp_check, self.da.check)


if __name__ == "__main__":
    unittest.main()
