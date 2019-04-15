"""
Unit test for suffix tree.

Jiangchen Zhu  <zjcsjtu@umich.edu>
"""
import substr_enc as se
import unittest


def get_common_prefix(str_1, str_2):
    """Compute the longest common prefix of two strings."""
    longest_prefix = ''
    if not str_1 or not str_2:
        return longest_prefix
    shorter_len = min(len(str_1), len(str_2))
    for i in range(shorter_len):
        if str_1[i] == str_2[i]:
            longest_prefix += str_1[i]
        else:
            break
    return longest_prefix


def check_node_sanity(node, is_root=False):
    """
    A valid node in suffix tree should satisfy.

    1. The edge label is non-empty, except for the root.
    2. Every internal node (node w/o children) has at least 2 children.
    3. No two edges out of a node have edge labels starting with 
       the same character.
    """
    # check rule 1
    if is_root:
        if node.edge_label:
            return False
    else:
        if not node.edge_label:
            return False
        # check rule 2, it should have 0 or at least 2 children
        num_child = len(node.children)
        if num_child == 1:
            return False

    # check rule 3
    children_edges = []
    for child in node.children:
        children_edges.append(child.edge_label)
    for i in range(len(children_edges)):
        for j in range(i + 1, len(children_edges)):
            if get_common_prefix(children_edges[i], children_edges[j]):
                return False
    return True


def check_all_nodes(tree):
    if not check_node_sanity(tree.root, is_root=True):
        return False
    tmp_list = list(tree.root.children)
    while tmp_list:
        next_children = []
        for child in tmp_list:
            if not check_node_sanity(child):
                return False
            next_children = next_children + list(child.children)
        tmp_list = next_children
    return True


class TestSuffixTree(unittest.TestCase):
    """Very simple test case."""
    def test_one(self):
        suffix_tree = se.utils.SuffixTree('cocoon')
        # self.assertEqual(len(suffix_tree.root.children), 3)
        # check the sanity of tree
        self.assertEqual(check_all_nodes(suffix_tree), True)