from bs4 import BeautifulSoup as bs
from pandas import DataFrame

class BaseLabel:
    """
    XMLラベルファイルを解析し、その内容をPandasのDataFrameに格納する基底クラスです。
    """
    def __init__(self, label_path:str = None) -> None:

        # ラベルファイルのパスを設定
        self.__label_path:str = label_path
        # BeautifulSoupでスクレイピング
        self.soup:bs = bs(open(label_path),features='xml') if label_path else None

        # データ取得先のリストを宣言
        self.__link_labels:DataFrame = None
        self.__link_locs:DataFrame = None
        self.__link_label_arcs:DataFrame = None

        # ラベルファイルのパスが設定済みの場合、タグを取得する
        self.__set_df()

    @property
    def label_path(self):
        return self.__label_path

    @label_path.setter
    def label_path(self, label_path:str):
        self.__label_path = label_path
        self.load_label_file(label_path)

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

    def load_label_file(self, path:str):
        with open(path, 'r', encoding='utf-8') as file:
            self.soup = bs(file, features='xml')
        self.__set_df()

    def __set_df(self):
        """
        ラベルパスが設定済みの場合、<link:label>、<link:loc>、<link:labelArc>タグを取得してDataFrameに格納します。
        """
        if self.label_path is not None:
            self.__link_labels = self.set_link_labels()
            self.__link_locs = self.set_link_locs()
            self.__link_label_arcs = self.set_link_label_arcs()

    def set_link_labels(self) -> DataFrame:
        pass

    def set_link_locs(self) -> DataFrame:
        pass

    def set_link_label_arcs(self) -> DataFrame:
        pass

class LocalLabel(BaseLabel):

    def __init__(self, label_path: str = None) -> None:
        super().__init__(label_path)

    def set_link_labels(self) -> DataFrame:
        """<link:label>要素からデータを抽出し、DataFrameを作成します。"""
        lists = []

        tags = self.soup.find_all(name='link:label')
        for tag in tags:
            dict = {
                'xml_lang': tag.get('xml:lang'),
                'xlink_type': tag.get('xlink:type'),
                'name_space': tag.get('xlink:label').split('_')[0],
                'xlink_label': tag.get('xlink:label').split('_')[1],
                'xlink_role': tag.get('xlink:role'),
                'xlink_text': tag.text
            }
            lists.append(dict)

        return DataFrame(lists)

    def set_link_locs(self) -> DataFrame:
        """<link:loc>要素からデータを抽出し、DataFrameを作成します。"""
        lists = []

        tags = self.soup.find_all(name='link:loc')
        for tag in tags:
            dict = {
                'xlink_type': tag.get('xlink:type'),
                'xlink:href': tag.get('xlink:href').split('#')[0],
                'name_space': tag.get('xlink:label').split('_')[0],
                'xlink_label': tag.get('xlink:label').split('_')[1]
            }
            lists.append(dict)

        return DataFrame(lists)

    def set_link_label_arcs(self) -> DataFrame:
        """<link:labelArc>要素からデータを抽出し、DataFrameを作成します。"""
        lists = []

        tags = self.soup.find_all(name='link:labelArc')
        for tag in tags:
            dict = {
                'xlink_type': tag.get('xlink:type'),
                'xlink_from_namespace': tag.get('xlink:from').split('_')[0],
                'xlink_from_label': tag.get('xlink:from').split('_')[1],
                'xlink_to_namespace': tag.get('xlink:to').split('_')[0],
                'xlink_to_label': '_'.join(tag.get('xlink:to').split('_')[1:]),
                'xlink_arcrole': tag.get('xlink:arcrole'),
                'order': tag.get('order')
            }
            lists.append(dict)

        return DataFrame(lists)

class GlobalLabel(BaseLabel):
    def __init__(self, label_path: str = None) -> None:
        super().__init__(label_path)

    def set_link_labels(self) -> DataFrame:
        lists = []

        tags = self.soup.find_all(name='link:label')
        for tag in tags:
            dict = {
                'xml_lang': tag.get('xml:lang'),
                'xlink_type': tag.get('xlink:type'),
                'xlink_label': '_'.join(tag.get('xlink:label').split('_')[1:]),
                'xlink_role': tag.get('xlink:role'),
                'id': tag.get('id'),
                'xlink_text': tag.text
            }

            lists.append(dict)

        return DataFrame(lists)

    def set_link_locs(self) -> DataFrame:
        lists = []
        
        tags = self.soup.find_all(name='link:loc')
        for tag in tags:
            dict = {
                'xlink_type': tag.get('xlink:type'),
                'xlink:href': tag.get('xlink:href'),
                
            }
        return super().set_link_locs()

    def set_link_label_arcs(self) -> DataFrame:
        return super().set_link_label_arcs()

if __name__ == '__main__':
    local_label_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-44440-2024-03-31-01-2024-05-14-lab.xml"
    global_label_path = "/Users/user/Vscode/python/PyXBRLTools/doc/taxnomy/jpcrp_2023-12-01_lab.xml"
    l_label = GlobalLabel(global_label_path)
    print(l_label.link_labels)
    l_label.link_labels.to_csv('hhh.csv')
