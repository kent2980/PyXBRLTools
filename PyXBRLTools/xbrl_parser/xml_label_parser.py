# 必要なライブラリのインポート
from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from abc import ABC, abstractmethod
import os

class BaseXmlLabelParser(ABC):
    """
    XMLラベルパーサの基底クラス。

    Attributes:
        file_path (str): パースするXMLファイルのパス。
        soup (BeautifulSoup): BeautifulSoupオブジェクト。
        __link_labels (DataFrame): link:label要素を含むDataFrame。
        __link_locs (DataFrame): link:loc要素を含むDataFrame。
        __link_label_arcs (DataFrame): link:labelArc要素を含むDataFrame。
    """

    def __init__(self, file_path: str) -> None:
        """初期化メソッド。

        Args:
            file_path (str): XMLファイルのパス。
        """
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as file:
            self.soup = bs(file, features='xml')
        self.__set_df()

    @property
    def link_labels(self):
        """link:label要素を含むDataFrameを返すプロパティ。"""
        return self.__link_labels

    @property
    def link_locs(self):
        """link:loc要素を含むDataFrameを返すプロパティ。"""
        return self.__link_locs

    @property
    def link_label_arcs(self):
        """link:labelArc要素を含むDataFrameを返すプロパティ。"""
        return self.__link_label_arcs

    def __set_df(self):
        """プライベートメソッド。DataFrameを設定する。"""
        if self.file_path:
            self.__link_labels = self.get_link_labels()
            self.__link_locs = self.get_link_locs()
            self.__link_label_arcs = self.get_link_label_arcs()

    def _get_tags_to_dataframe(self, tag_names: list) -> DataFrame:
        """タグ名のリストからDataFrameを生成するヘルパーメソッド。

        Args:
            tag_names (list): タグ名のリスト。

        Returns:
            DataFrame: 生成されたDataFrame。
        """
        tags = self.soup.find_all(name=tag_names)
        data_list = [
            {key.replace(':', '_'): tag.get(key) for key in tag.attrs.keys()} | {'text': tag.text}
            for tag in tags
        ]
        return DataFrame(data_list)

    @abstractmethod
    def get_link_labels(self) -> DataFrame:
        """link:label要素を取得する抽象メソッド。"""
        pass

    @abstractmethod
    def get_link_locs(self) -> DataFrame:
        """link:loc要素を取得する抽象メソッド。"""
        pass

    @abstractmethod
    def get_link_label_arcs(self) -> DataFrame:
        """link:labelArc要素を取得する抽象メソッド。"""
        pass

class XmlLabelParser(BaseXmlLabelParser):
    """BaseXmlLabelParserを継承して具体的な実装を行うクラス。"""

    def get_link_labels(self) -> DataFrame:
        """link:label要素を取得するメソッド。"""
        return self._get_tags_to_dataframe(['link:label', 'label'])

    def get_link_locs(self) -> DataFrame:
        """link:loc要素を取得するメソッド。"""
        lists = []

        tags = self.soup.find_all(name=['link:loc', 'loc'])
        for tag in tags:
            dict = {
                'xlink_type': tag.get('xlink:type'),
                'xlink_schema': tag.get('xlink:href').split('#')[0],
                'xlink_href': tag.get('xlink:href').split('#')[-1:][0],
                'xlink_label': tag.get('xlink:label'),
                'text': tag.text
            }
            lists.append(dict)
        return DataFrame(lists)

    def get_link_label_arcs(self) -> DataFrame:
        """link:labelArc要素を取得するメソッド。"""
        return self._get_tags_to_dataframe(['link:labelArc', 'labelArc'])

if __name__ == '__main__':
    # ファイルパスの設定
    local_file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-57210-2024-03-31-01-2024-05-13-lab.xml"
    global_file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/taxonomy/jppfs/2023-12-01/label/jppfs_2023-12-01_lab.xml"

    # XmlLabelクラスのインスタンス化
    gl_label = XmlLabelParser(global_file_path)
    lo_label = XmlLabelParser(local_file_path)

    # 出力ディレクトリの作成
    output_dir = "extract_csv/label"
    os.makedirs(output_dir, exist_ok=True)

    # CSVファイルへの出力
    gl_label.link_locs.to_csv(f'{output_dir}/gl_link_locs.csv', encoding='utf-8-sig')
    gl_label.link_label_arcs.to_csv(f'{output_dir}/gl_label_arcs.csv', encoding='utf-8-sig')
    gl_label.link_labels.to_csv(f'{output_dir}/gl_label.csv', encoding='utf-8-sig')

    lo_label.link_locs.to_csv(f'{output_dir}/lo_link_locs.csv', encoding='utf-8-sig')
    lo_label.link_label_arcs.to_csv(f'{output_dir}/lo_label_arcs.csv', encoding='utf-8-sig')
    lo_label.link_labels.to_csv(f'{output_dir}/lo_label.csv', encoding='utf-8-sig')
