"""
A simple implementation of a suffix tree,
used in Substring-Searchable Encryption.

Jiangchen Zhu  <zjcsjtu@umich.edu>
"""
from substr_enc.utils.suffix_tree_helper import get_path_helper, get_common_prefix
from substr_enc.utils.suffix_tree_helper import get_initial_path_helper

class Node:
    """Represent a node in suffix tree."""
    def __init__(self):
        """Initialize the node."""
        self.edge_label = ''
        self.parent = None
        self.children = set()
        # if this is a leaf node, leaf_label represents the starting index
        self.leaf_label = -1
    
    
    def get_path(self):
        """Call the helper function and return the path label."""
        return get_path_helper(self)
    

    def get_initial_path(self):
        """Call the helper function and return the initial path label."""
        return get_initial_path_helper(self)


def init_helper(cur_node, suffix, index):
    """Helper function for init method, recursively go down the tree."""
    if suffix == '':
        return
    target_child = None
    # check if there exists an edge starts with the same prefix
    for child in cur_node.children:
        prefix_tmp = get_common_prefix(suffix, child.edge_label)
        if prefix_tmp:
            target_child = child
            break
    
    # if we cannot find a child starts with the same prefix
    if target_child == None:
        target_child = Node()
        # the cur_node is no longer a leaf node
        cur_node.leaf_label = -1
        cur_node.children.add(target_child)
        # make a new child for the suffix
        target_child.parent = cur_node
        target_child.edge_label = suffix
        target_child.leaf_label = index
        return
    else:
        common_prefix = get_common_prefix(suffix, target_child.edge_label)
        common_pre_len = len(common_prefix)
        if common_pre_len < len(target_child.edge_label):
            # if the length of common prefix is shorter than the edge of 
            # target child, then,
            # need to split the target_child into two nodes
            new_node = Node()
            new_node.leaf_label = target_child.leaf_label
            new_node.children = target_child.children.copy()
            new_node.edge_label = target_child.edge_label[common_pre_len:]
            target_child.leaf_label = -1
            target_child.children.clear()
            target_child.children.add(new_node)
            target_child.edge_label = common_prefix
            new_node.parent = target_child
            init_helper(target_child, suffix[common_pre_len:], index)
        else:
            # recursively build the tree for suffix
            init_helper(target_child, suffix[common_pre_len:], index)


class SuffixTree:
    """Implement a suffix tree according to the paper."""
    def __init__(self, s):
        """Build a suffix tree given string s."""
        # insert dollar sign to make sure that a suffix tree exists
        # assume that $ does not appear in string s
        s += '$'
        self.root = Node()
        # create nodes for every suffix
        for i in range(2, len(s) + 1):
            sufx = s[-i:]
            init_helper(cur_node=self.root, suffix=sufx, index=len(s) - i)


    def show_tree(self):
        """Print the suffix tree level by level for debug."""
        print('Printing the suffix tree level by level...')
        tmp_list = list(self.root.children)
        ind = 1
        while tmp_list:
            print('level', ind)
            next_children = []
            for child in tmp_list:
                print(child.edge_label, '\t', child.leaf_label)
                next_children = next_children + list(child.children)
            tmp_list = next_children
            ind += 1
        print('------------------------------------------------')
