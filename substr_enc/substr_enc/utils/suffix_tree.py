"""
A simple implementation of a suffix tree, as specified in the paper,
used in Substring-Searchable Encryption.

Jiangchen Zhu  <zjcsjtu@umich.edu>
"""
from substr_enc.utils.suffix_tree_helper import get_path_helper, get_common_prefix
from substr_enc.utils.suffix_tree_helper import get_initial_path_helper
from substr_enc.utils.suffix_tree_helper import get_ind_helper

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
        """Call the helper function and return the path label (incl. $)."""
        return get_path_helper(self)
    

    def get_initial_path(self):
        """Call the helper function and return the initial path label."""
        return get_initial_path_helper(self)

    
    def get_len(self):
        """Return he length of inital path (may incl. $)."""
        return len(self.get_initial_path())
    

    def get_ind(self):
        """Return the index in string of the first occurrence of path label."""
        node_inds = []
        get_ind_helper(self, node_inds)
    

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


def get_leaves_helper(node, output):
    """Preorder traverse the tree and get the leaf nodes rooted at this node."""
    if node == None:
        return
    if not node.children:
        output.append(node)
    for child in node.children:
        get_leaves_helper(child, output)


class SuffixTree:
    """Implement a suffix tree according to the paper."""
    def __init__(self, s):
        """Build a suffix tree given string s."""
        # insert dollar sign to make sure that a suffix tree exists
        # assume that $ does not appear in string s
        s += '$'
        self.root = Node()
        self.leaves = []
        # create nodes for every suffix
        for i in range(2, len(s) + 1):
            sufx = s[-i:]
            init_helper(cur_node=self.root, suffix=sufx, index=len(s) - i)
        get_leaves_helper(self.root, self.leaves)
    

    def get_leafpos(self, node):
        """
        Return the position (between 0 and n - 1) in the
        tree of the leftmost leaf in the subtree rooted at node.
        """
        # get all leaves that are rooted at node
        leaves_rooted_node = []
        get_leaves_helper(node, leaves_rooted_node)
        min_leafpos = len(self.leaves)
        for leaf in leaves_rooted_node:
            leaf_ind = self.leaves.index(leaf)
            if leaf_ind < min_leafpos:
                min_leafpos = leaf_ind
        return min_leafpos
    

    def get_num(self, node):
        """Return number of leaves in the subtree rooted at node."""
        leaves_rooted_node = []
        get_leaves_helper(node, leaves_rooted_node)
        return len(leaves_rooted_node)


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
