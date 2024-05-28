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

    def __init__(self, file_path: str = None) -> None:
        """初期化メソッド。

        Args:
            file_path (str): XMLファイルのパス。
        """
        if not file_path == None:
            self.__file_path = file_path
            with open(file_path, 'r', encoding='utf-8') as file:
                self.soup = bs(file, 'lxml-xml')

    @property
    def file_path(self) -> str:
        """file_path属性のゲッター。"""
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path: str) -> None:
        """file_path属性のセッター。

        Args:
            file_path (str): パースするXMLファイルのパス。
        """
        self.__file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as file:
            self.soup = bs(file, 'lxml-xml')

    def _get_tags_to_dataframe(self, tag_names: list) -> DataFrame:
        """タグ名のリストからDataFrameを生成するヘルパーメソッド。

        Args:
            tag_names (list): タグ名のリスト。

        Returns:
            DataFrame: 生成されたDataFrame。

        example:
        tag_names = ['link:label', 'label']
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
    """ XMLラベルパーサの具象クラス。XMLラベルの情報を取得するクラス。"""

    def get_link_labels(self) -> DataFrame:
        """link:label要素を取得するメソッド。

        returns:
            DataFrame: link:label要素を含むDataFrame。

        example:
        get_link_labels()の出力例
        >>> df = get_link_labels()
            print(df)
        output:
        |    | xlink_type | xlink_role | xlink_label | text |
        |----|------------|------------|-------------|------|
        | 0  | label      | http://www.xbrl.org/2003/role/label | jppfs_lab_EquityClassOfShares | 株式の種類 |
        | 1  | label      | http://www.xbrl.org/2003/role/label | jppfs_lab_EquityClassOfShares | 株式の種類 |
        | 2  | label      | http://www.xbrl.org/2003/role/label | jppfs_lab_EquityClassOfShares | 株式の種類 |
        """
        return self._get_tags_to_dataframe(['link:label', 'label'])

    # def get_link_locs(self) -> DataFrame:
    #     """link:loc要素を取得するメソッド。

    #     returns:
    #         DataFrame: link:loc要素を含むDataFrame。

    #     example:
    #     get_link_locs()の出力例
    #     >>> df = get_link_locs()
    #         print(df)
    #     output:
    #     |    | xlink_type | xlink_schema | xlink_href | xlink_label | text |
    #     |----|------------|------------|-------------|------|
    #     | 0  | locator    | jppfs_cor_2023-12-01.xsd | jppfs_cor_EquityClassOfShares | EquityClassOfShares |  |
    #     | 1  | locator    | jppfs_cor_2023-12-01.xsd | jppfs_cor_EquityClassOfShares | EquityClassOfShares |  |
    #     | 2  | locator    | jppfs_cor_2023-12-01.xsd | jppfs_cor_EquityClassOfShares | EquityClassOfShares |  |
    #     """
    #     lists = []

    #     tags = self.soup.find_all(name=['link:loc', 'loc'])
    #     for tag in tags:
    #         dict = {
    #             'xlink_type': tag.get('xlink:type'),
    #             'xlink_schema': tag.get('xlink:href').split('#')[0],
    #             'xlink_href': tag.get('xlink:href').split('#')[-1:][0],
    #             'xlink_label': tag.get('xlink:label'),
    #             'text': tag.text
    #         }
    #         lists.append(dict)
    #     return DataFrame(lists)

    def get_link_locs(self, element_name:str = None) -> DataFrame:
        """link:loc要素を取得するメソッド。

        returns:
            DataFrame: link:loc要素を含むDataFrame。

        example:
        get_link_locs()の出力例
        >>> df = get_link_locs(element_name='jppfs_cor_EquityClassOfShares')
            print(df)
        output:
        |    | xlink_type | xlink_schema | xlink_href | xlink_label | text |
        |----|------------|------------|-------------|------|
        | 0  | locator    | jppfs_cor_2023-12-01.xsd | jppfs_cor_EquityClassOfShares | EquityClassOfShares |  |
        | 1  | locator    | jppfs_cor_2023-12-01.xsd | jppfs_cor_EquityClassOfShares | EquityClassOfShares |  |
        | 2  | locator    | jppfs_cor_2023-12-01.xsd | jppfs_cor_EquityClassOfShares | EquityClassOfShares |  |
        """
        lists = []
        tags = None

        if element_name == None:
            tags = self.soup.find_all(name=['link:loc', 'loc'])
        else:
            # self.soupからxlink_hrefプロパティがxlink_hrefの値と一致する要素を取得
            tags = self.soup.find_all(name=['link:loc', 'loc'], attrs={'xlink:label': element_name})
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
        """link:labelArc要素を取得するメソッド。

        returns:
            DataFrame: link:labelArc要素を含むDataFrame。

        example:
        get_link_label_arcs()の出力例
        >>> df = get_link_label_arcs()
            print(df)
        output:
        |    | xlink_type | xlink_arcrole | xlink_from | xlink_to | text |
        |----|------------|---------------|------------|----------|------|
        | 0  | arc        | http://www.xbrl.org/2003/arcrole/concept-label | jppfs_cor_EquityClassOfShares | jppfs_lab_EquityClassOfShares | |
        | 1  | arc        | http://www.xbrl.org/2003/arcrole/concept-label | jppfs_cor_EquityClassOfShares | jppfs_lab_EquityClassOfShares | |
        | 2  | arc        | http://www.xbrl.org/2003/arcrole/concept-label | jppfs_cor_EquityClassOfShares | jppfs_lab_EquityClassOfShares | |
        """
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
    gl_label.get_link_locs().to_csv(f'{output_dir}/gl_link_locs.csv', encoding='utf-8-sig')
    gl_label.get_link_label_arcs().to_csv(f'{output_dir}/gl_label_arcs.csv', encoding='utf-8-sig')
    gl_label.get_link_labels().to_csv(f'{output_dir}/gl_label.csv', encoding='utf-8-sig')

    lo_label.get_link_locs().to_csv(f'{output_dir}/lo_link_locs.csv', encoding='utf-8-sig')
    lo_label.get_link_label_arcs().to_csv(f'{output_dir}/lo_label_arcs.csv', encoding='utf-8-sig')
    lo_label.get_link_labels().to_csv(f'{output_dir}/lo_label.csv', encoding='utf-8-sig')
