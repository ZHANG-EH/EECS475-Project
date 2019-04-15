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
    """Check all nodes sanity."""
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


def traverse_tree(node, cumul_suffix, output):
    """Preorder traverse the tree and get all possible suffices."""
    if node == None:
        return
    print(node.edge_label)
    if not node.children:
        output[node.leaf_label] = cumul_suffix + node.edge_label
    for child in node.children:
        tmp = cumul_suffix + node.edge_label
        traverse_tree(child, tmp, output)


def get_all_suffices(tree):
    """Return all suffices in this tree."""
    ret_suffices = {}
    traverse_tree(tree.root, '', ret_suffices)
    return ret_suffices


def check_suffices(suffices, full_str):
    """Check if suffices contain all suffix of the string, with correct leaf label."""
    if len(suffices) != len(full_str) - 1:
        return False
    for index in suffices:
        correct_suffix = full_str[index:]
        student_suffix = suffices[index]
        if correct_suffix != student_suffix:
            return False
    return True


class TestSuffixTree(unittest.TestCase):

    def test_1(self):
        test_str = 'cocoon'
        suffix_tree = se.utils.SuffixTree(test_str)
        # check the sanity of tree
        self.assertEqual(check_all_nodes(suffix_tree), True)
        # check that the tree gives the correct suffices
        suffices = get_all_suffices(suffix_tree)
        self.assertEqual(check_suffices(suffices, test_str + '$'), True)

    def test_2(self):
        test_str = 'We hold these truths to be self-evident, that all men are created equal, that they are endowed by their Creator with certain unalienable Rights, that among these are Life, Liberty and the pursuit of Happiness.'
        suffix_tree = se.utils.SuffixTree(test_str)
        # check the sanity of tree
        self.assertEqual(check_all_nodes(suffix_tree), True)
        # check that the tree gives the correct suffices
        suffices = get_all_suffices(suffix_tree)
        self.assertEqual(check_suffices(suffices, test_str + '$'), True)

    def test_3(self):
        test_str = 'Hello, this is our project. We are attempting to build a substring searchable encryption system.'
        suffix_tree = se.utils.SuffixTree(test_str)
        # check the sanity of tree
        self.assertEqual(check_all_nodes(suffix_tree), True)
        # check that the tree gives the correct suffices
        suffices = get_all_suffices(suffix_tree)
        self.assertEqual(check_suffices(suffices, test_str + '$'), True)

    def test_4(self):
        test_str = 'aflkjaieaufodafjoewiajadfkjafjkjkdsaljd aldjflkjdaf ladjflkdajf ldsa fadjfklaf'
        suffix_tree = se.utils.SuffixTree(test_str)
        # check the sanity of tree
        self.assertEqual(check_all_nodes(suffix_tree), True)
        # check that the tree gives the correct suffices
        suffices = get_all_suffices(suffix_tree)
        self.assertEqual(check_suffices(suffices, test_str + '$'), True)
