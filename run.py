import substr_enc as se


def main():
    """Run the paper example."""
    print('test 1')
    suffix_tree = se.utils.SuffixTree('cocoon')
    suffix_tree.show_tree()
    r = suffix_tree.root
    print(r.edge_label, r.get_path(), r.get_initial_path())
    tmp_list = list(r.children)
    while tmp_list:
        next_children = []
        for child in tmp_list:
            print(child.edge_label, child.get_path(), child.get_initial_path())
            next_children = next_children + list(child.children)
        tmp_list = next_children


if __name__ == '__main__':
    main()