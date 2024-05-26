# 必要なライブラリのインポート
from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from abc import ABC, abstractmethod
import os

class BaseXmlLinkParser(ABC):
    """
    XMLラベルパーサの基底クラス。

    Attributes:
        file_path (str): パースするXMLファイルのパス。
        soup (BeautifulSoup): BeautifulSoupオブジェクト。
        __link_labels (DataFrame): link:label要素を含むDataFrame。
        __link_locs (DataFrame): link:loc要素を含むDataFrame。
        __link_arcs (DataFrame): link:labelArc要素を含むDataFrame。
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
    def link_locs(self):
        """link:loc要素を含むDataFrameを返すプロパティ。"""
        return self.__link_locs

    @property
    def link_arcs(self):
        """link:labelArc要素を含むDataFrameを返すプロパティ。"""
        return self.__link_arcs

    def __set_df(self):
        """プライベートメソッド。DataFrameを設定する。"""
        if self.file_path:
            self.__link_locs = self.get_link_locs()
            self.__link_arcs = self.get_link_arcs()

    def _get_tags_to_dataframe(self, tag_names: list) -> DataFrame:
        """タグ名のリストからDataFrameを生成するヘルパーメソッド。

        Args:
            tag_names (list): タグ名のリスト。

        Returns:
            DataFrame: 生成されたDataFrame。
        """
        tags = self.soup.find_all(name=tag_names)
        data_list = [
            {key: tag.get(key) for key in tag.attrs.keys()} | {'text': tag.text}
            for tag in tags
        ]
        return DataFrame(data_list)

    @abstractmethod
    def get_link_locs(self) -> DataFrame:
        """link:loc要素を取得する抽象メソッド。"""
        pass

    @abstractmethod
    def get_link_arcs(self) -> DataFrame:
        """link:labelArc要素を取得する抽象メソッド。"""
        pass

class XmlLinkParser(BaseXmlLinkParser):
    """BaseXmlLabelParserを継承して具体的な実装を行うクラス。"""

    def get_link_locs(self) -> DataFrame:
        """link:loc要素を取得するメソッド。"""
        return self._get_tags_to_dataframe(['link:loc', 'loc'])

    def get_link_arcs(self) -> DataFrame:
        """link:labelArc要素を取得するメソッド。"""
        tag_list = ['link:calculationArc','link:definitionArc','link:presentationArc']
        return self._get_tags_to_dataframe(tag_list)

if __name__ == '__main__':
    # ファイルパスの設定
    pre_file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-57210-2024-03-31-01-2024-05-13-pre.xml"
    cal_file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-57210-2024-03-31-01-2024-05-13-cal.xml"
    def_file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-57210-2024-03-31-01-2024-05-13-def.xml"
    # XmlLabelクラスのインスタンス化
    pre_label = XmlLinkParser(pre_file_path)
    cal_label = XmlLinkParser(cal_file_path)
    def_label = XmlLinkParser(def_file_path)

    # 出力ディレクトリの作成
    output_dir = "extract_csv/link"
    os.makedirs(output_dir, exist_ok=True)

    # CSVファイルへの出力
    pre_label.link_locs.to_csv(f'{output_dir}/pre_link_locs.csv', encoding='utf-8-sig')
    pre_label.link_arcs.to_csv(f'{output_dir}/pre_arcs.csv', encoding='utf-8-sig')

    cal_label.link_locs.to_csv(f'{output_dir}/cal_link_locs.csv', encoding='utf-8-sig')
    cal_label.link_arcs.to_csv(f'{output_dir}/cal_arcs.csv', encoding='utf-8-sig')

    def_label.link_locs.to_csv(f'{output_dir}/def_link_locs.csv', encoding='utf-8-sig')
    def_label.link_arcs.to_csv(f'{output_dir}/def_arcs.csv', encoding='utf-8-sig')