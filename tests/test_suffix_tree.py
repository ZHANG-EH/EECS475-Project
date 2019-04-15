import substr_enc as se
import unittest

class TestSuffixTree(unittest.TestCase):
    """Very simple test case."""
    def test_one(self):
        print('test 1')
        suffix_tree = se.utils.SuffixTree('cocoon')
        suffix_tree.show_tree()
        self.assertEqual(len(suffix_tree.root.children), 3)