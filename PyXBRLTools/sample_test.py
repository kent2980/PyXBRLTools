from xbrl_manager.ixbrl_manager import IxbrlManager

if __name__ == '__main__':

    xbrl_direrctory_path = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData'
    load_xbrl_directory_path = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir'

    manager = IxbrlManager(xbrl_direrctory_path)
    print(manager.ix_non_fractions)
    print(manager.ix_non_numerics)
    print(manager.xbrli_contexts)