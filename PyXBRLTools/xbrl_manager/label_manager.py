# from xbrl_parser.xml_label_parser import XmlLabelParser
import os
from xbrl_manager.base_xbrl_manager import BaseXbrlManager
from xbrl_parser.xml_schema_parser import XmlSchemaParser

class BaseLabelManager(BaseXbrlManager):
    """ labelファイルの情報を取得するクラス。"""

    def __init__(self, dir_path: str):
        """ コンストラクタ """
        super().__init__(dir_path)
        self.__get_label_path()

    def __get_label_path(self) -> str:
        """ labelファイルのパスを取得するメソッド。"""
        for schema_file in self.schema_files:
            print(schema_file['path'])
            schema_parser = XmlSchemaParser(schema_file['path'])
            print(schema_parser.link_base_refs['xlink_href'].to_list())

class LabelManager(BaseLabelManager):
    pass

# テストコード
if __name__ == "__main__":
    print("Test sample")

    dir_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData"
    label_manager = BaseLabelManager(dir_path)
    print(label_manager.schema_files)