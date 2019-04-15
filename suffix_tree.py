"""
A simple implementation of a suffix tree,
used in Substring-Searchable Encryption.

Jiangchen Zhu  <zjcsjtu@umich.edu>
"""

class Node:
    """Represent a node in suffix tree."""
    def __init__(self):
        """Initialize the node."""
        self.edge_label = ''
        self.parent = None
        self.children = set()
        # if this is a leaf node, leaf_label represents the starting index
        self.leaf_label = -1


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
            self.init_helper(cur_node=self.root, suffix=sufx, index=len(s) - i)
    
    def init_helper(self, cur_node, suffix, index):
        """Helper function for init method, recursively go down the tree."""
        if suffix == '$':
            return
        target_child = None
        # check if there exists an edge starts with the same prefix
        for child in self.root.children:
            prefix_tmp = get_common_prefix(suffix, child.edge_label)
            if prefix_tmp:
                target_child = child
        
        # if we cannot find a child starts with the same prefix
        if target_child == None:
            target_child = Node()
            # the cur_node is no longer a leaf node
            cur_node.leaf_label = -1
            cur_node.children.add(target_child)
            # make a new child
            target_child.parent = cur_node
            target_child.edge_label = suffix
            target_child.leaf_label = index
        else:
            common_prefix = get_common_prefix(suffix, target_child.edge_label)
            common_pre_len = len(common_prefix)
            # need to split the cur_node into two nodes
            new_node = Node()
            new_node.leaf_label = target_child.leaf_label
            new_node.children = target_child.children.copy()
            new_node.edge_label = target_child.edge_label[common_pre_len:]
            target_child.leaf_label = -1
            target_child.children.clear()
            target_child.children.add(new_node)
            target_child.edge_label = common_prefix
            new_node.parent = target_child
            # create another node for the suffix
            suf_node = Node()
            suf_node.leaf_label = index
            suf_node.edge_label = suffix[common_pre_len:]
            suf_node.parent = target_child

    def show_tree(self):
        """Print the suffix tree level by level for debug."""
        print('Printing the suffix tree...')
        tmp_list = list(self.root.children)
        print(tmp_list)
        ind = 1
        while tmp_list:
            print(ind)
            next_children = []
            for child in tmp_list:
                print(child.edge_label, '\t', child.leaf_label)
                next_children = next_children + list(child.children)
            tmp_list = next_children
            ind += 1


def main():
    print('simple test')
    suffix_tree = SuffixTree('cocoon')
    suffix_tree.show_tree()


if __name__ == '__main__':
    main()