from xbrl_parser.ixbrl_parser import IxbrlParser
from xbrl_manager.ixbrl_manager import IxbrlManager
import os
# テストコード
if __name__ == "__main__":
    # osがwindowsの場合
    if os.name == 'nt':
        dir = "C:/Users/kent2/OneDrive/ドキュメント/vscode/python/PyXBRLTools/doc/XBRLData"
    # osがmacの場合
    elif os.name == 'posix':
        dir = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData"

    ix_manager = IxbrlManager(dir)
    print(ix_manager.set_ix_non_fraction("pl").to_DataFrame())
    print(ix_manager.set_ix_non_numeric("sm").to_DataFrame())
    print(ix_manager.set_ix_non_numeric("bs").to_DataFrame())