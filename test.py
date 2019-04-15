import substr_enc as se


def main():
    print('simple test')
    suffix_tree = se.utils.SuffixTree('cocoon')
    suffix_tree.show_tree()


if __name__ == '__main__':
    main()