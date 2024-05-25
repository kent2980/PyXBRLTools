from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from abc import ABC, abstractmethod

class BaseXmlLabelParser(ABC):
    """
    XMLラベルファイルを解析し、その内容をPandasのDataFrameに格納する基底クラスです。
    """
    def __init__(self, file_path:str) -> None:

        # ラベルファイルのパスを設定
        self.__file_path:str = file_path
        # BeautifulSoupでスクレイピング
        self.soup = bs(open(file_path),features='xml')

        self.__link_labels = None
        self.__link_locs = None
        self.__link_label_arcs = None

        # ラベルファイルのパスが設定済みの場合、タグを取得する
        self.__set_df()

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path:str):
        self.__file_path = file_path
        self.soup = bs(open(file_path), features='xml')
        self.__set_df()

    @property
    def link_labels(self):
        """<link:label>要素を含むDataFrameを取得します。"""
        return self.__link_labels

    @property
    def link_locs(self):
        """<link:loc>要素を含むDataFrameを取得します。"""
        return self.__link_locs

    @property
    def link_label_arcs(self):
        """<link:labelArc>要素を含むDataFrameを取得します。"""
        return self.__link_label_arcs

    def __set_df(self):
        """
        ラベルパスが設定済みの場合、<link:label>、<link:loc>、<link:labelArc>タグを取得してDataFrameに格納します。
        """
        if self.file_path is not None:
            self.__link_labels = self.get_link_labels()
            self.__link_locs = self.get_link_locs()
            self.__link_label_arcs = self.get_link_label_arcs()

    @abstractmethod
    def get_link_labels(self) -> DataFrame:
        pass

    @abstractmethod
    def get_link_locs(self) -> DataFrame:
        pass

    @abstractmethod
    def get_link_label_arcs(self) -> DataFrame:
        pass

class XmlLocalLabel(BaseXmlLabelParser):

    def __init__(self, file_path: str = None) -> None:
        super().__init__(file_path)

    def get_link_labels(self) -> DataFrame:
        """<link:label>要素からデータを抽出し、DataFrameを作成します。"""
        lists = []

        tags = self.soup.find_all(name='link:label')
        for tag in tags:
            dict = {
                'xml_lang': tag.get('xml:lang'),
                'xlink_type': tag.get('xlink:type'),
                'xlink_label': tag.get('xlink:label'),
                'xlink_role': tag.get('xlink:role'),
                'xlink_text': tag.text
            }
            lists.append(dict)

        return DataFrame(lists)

    def get_link_locs(self) -> DataFrame:
        """<link:loc>要素からデータを抽出し、DataFrameを作成します。"""
        lists = []

        tags = self.soup.find_all(name='link:loc')
        for tag in tags:
            dict = {
                'xlink_type': tag.get('xlink:type'),
                'xlink_href': tag.get('xlink:href'),
                'xlink_label': tag.get('xlink:label')
            }
            lists.append(dict)

        return DataFrame(lists)

    def get_link_label_arcs(self) -> DataFrame:
        """<link:labelArc>要素からデータを抽出し、DataFrameを作成します。"""
        lists = []

        tags = self.soup.find_all(name='link:labelArc')
        for tag in tags:
            dict = {
                'xlink_type': tag.get('xlink:type'),
                'xlink_from': tag.get('xlink:from').split('_')[0],
                'xlink_to': tag.get('xlink:to').split('_')[0],
                'xlink_arcrole': tag.get('xlink:arcrole'),
                'order': tag.get('order')
            }
            lists.append(dict)

        return DataFrame(lists)

class XmlGlobalLabel(BaseXmlLabelParser):
    def __init__(self, file_path: str = None) -> None:
        super().__init__(file_path)

    def get_link_labels(self) -> DataFrame:
        lists = []

        tags = self.soup.find_all(name='link:label')
        for tag in tags:
            dict = {
                'xml_lang': tag.get('xml:lang'),
                'xlink_type': tag.get('xlink:type'),
                'xlink_label': tag.get('xlink:label'),
                'xlink_role': tag.get('xlink:role'),
                'id': tag.get('id'),
                'xlink_text': tag.text
            }

            lists.append(dict)

        return DataFrame(lists)

    def get_link_locs(self) -> DataFrame:
        lists = []

        tags = self.soup.find_all(name='link:loc')
        for tag in tags:
            dict = {
                'xlink_type': tag.get('xlink:type'),
                'xlink_href': tag.get('xlink:href'),
                'xlink_label': tag.get('xlink:label')
            }

            lists.append(dict)

        return DataFrame(lists)

    def get_link_label_arcs(self) -> DataFrame:
        lists = []

        tags = self.soup.find_all(name='link:labelArc')
        for tag in tags:
            dict = {
                'xlink_type': tag.get('xlink:type'),
                'xlink_arcrole': tag.get('xlink:arcrole'),
                'xlink_from': tag.get('xlink:from'),
                'xlink_to': tag.get('xlink:to')
            }

            lists.append(dict)

        return DataFrame(lists)

if __name__ == '__main__':
    local_file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-44440-2024-03-31-01-2024-05-14-lab.xml"
    global_file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/taxnomy/jpcrp_2023-12-01_lab.xml"
    l_label = XmlGlobalLabel(global_file_path)
    print(l_label.link_labels)
    l_label.link_locs.to_csv('hhh.csv')
