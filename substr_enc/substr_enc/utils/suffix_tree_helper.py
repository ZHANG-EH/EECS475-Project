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
        return node.get_path(node.parent) + node.edge_label


def get_initial_path_helper(node):
    """Compute the initial path label of a node recursively."""
    if node.parent == None:
        # if this is a root node
        return ''
    else:
        return node.parent.get_path() + node.edge_label

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
