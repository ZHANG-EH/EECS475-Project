"""
Helper functions for suffix tree.

Jiangchen Zhu  <zjcsjtu@umich.edu>
"""

def get_path_helper(node):
    """Compute the path label of a node recursively."""
    if node.parent == None:
        # if this is a root node
        return ''
    else:
        return get_path_helper(node.parent) + node.edge_label


def get_initial_path_helper(node):
    """Compute the initial path label of a node recursively."""
    if node.parent == None:
        # if this is a root node
        return ''
    else:
        return node.parent.get_path() + node.edge_label[0]


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


def get_ind_helper(node, output):
    """Preorder traverse the tree and get the indices of the node."""
    if node == None:
        return
    if not node.children:
        output.append(node.leaf_label)
    for child in node.children:
        get_ind_helper(child, output)
