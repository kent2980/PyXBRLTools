from xbrl_parser.ixbrl_parser import IxbrlParser
from xbrl_manager.ixbrl_manager import IxbrlManager
import os
# テストコード
if __name__ == "__main__":
#     file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Summary/tse-acedjpsm-58200-20240327560965-ixbrl.htm"
#     parser = IxbrlParser.create(file_path)
    # print('ix_non_numeric**************************')
    # print(parser.ix_non_numeric().to_DataFrame())
    # print('ix_non_fractions**************************')
    # print(parser.ix_non_fractions().to_DataFrame())
    # osがwindowsの場合
    if os.name == 'nt':
        dir = "C:/Users/kent2/OneDrive/ドキュメント/vscode/python/PyXBRLTools/doc/XBRLData"
    # osがmacの場合
    elif os.name == 'posix':
        dir = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData"

    ix_manager = IxbrlManager(dir)
    print(ix_manager.set_document_type("sm").set_ix_non_fraction().to_DataFrame())
    print(ix_manager.set_document_type("bs").set_ix_non_numeric().to_DataFrame())
    print(ix_manager.set_ix_non_numeric().to_DataFrame())