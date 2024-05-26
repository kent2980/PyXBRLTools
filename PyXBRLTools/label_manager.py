from xbrl_parser.xbrl_parser_controller import XbrlParserController
import os
from utils import Utils
import pandas as pd
from abc import ABC, abstractmethod
import time

class BaseLabelManager(ABC):
    """
    XBRLラベルの基底クラスです。

    Attributes:
        dir_path (str): ディレクトリのパス。
    """

    def __init__(self, dir_path:str):
        self.__dir_path = dir_path

    @property
    def dir_path(self):
        """ディレクトリのパスを取得します。"""
        return self.__dir_path

    @abstractmethod
    def get_link_label(self, xlink_href:str):
        """
        xlink:href属性に基づいてラベルを取得するための抽象メソッドです。

        Args:
            xlink_href (str): 取得したいラベルのxlink:href属性。

        Returns:
            実装に依存します。
        """
        pass

class LabelManager(BaseLabelManager):
    """
    XBRLラベルを管理するためのクラスです。

    BaseLabelManager を継承しています。
    """

    def __get_xlink_href(self, name_space) -> str | None:
        """
        指定された名前空間に対応するリンクベース参照を含むファイルの xlink:href 属性を返します。

        Args:
            name_space (str): 名前空間の文字列。

        Returns:
            str | None: 見つかった場合はxlink:href属性の値、見つからなければNone。
        """

        # 指定されたディレクトリ内で正規表現にマッチするファイル名を検索します。
        files = Utils.find_filename_with_regex(self.dir_path, "^.*xsd$")
        if not files:  # Early return if no files are found
            return None

        # Collect parser DataFrames in a list
        parser_dfs = []
        for file in files:
            parser = XbrlParserController.xml_schema_parser(file)
            parser_df = parser.link_base_refs
            parser_dfs.append(parser_df)

        # Concatenate all DataFrames at once
        combined_df = pd.concat(parser_dfs, ignore_index=True)

        # Use query with regex to filter rows
        query_string = f"xlink_role == 'http://www.xbrl.org/2003/role/labelLinkbaseRef' and xlink_href.str.contains(r'{name_space}.*lab\.xml$', regex=True)"
        filtered_df = combined_df.query(query_string)

        if not filtered_df.empty:
            value = filtered_df.iloc[0]['xlink_href']
            return value
        else:
            return None

    def __get_local_file_path(self, label_path:str) -> str:
        """
        ローカルファイルシステム上でのラベルファイルのパスを取得します。

        Args:
            label_path (str): ラベルファイルのパス。

        Returns:
            str: ファイルのフルパス。
        """

        file_path = ""
        for root, dirs, files in os.walk(self.dir_path):
            if label_path in files:
                file_path = os.path.join(root, label_path)

        return file_path

    def __get_global_file_path(self, label_path:str) -> str:
        """
        グローバルファイルシステム上でのラベルファイルのパスを取得し、必要に応じてダウンロードします。

        Args:
            label_path (str): ラベルファイルのURL。

        Returns:
            str: ダウンロード後のファイルのローカルパス。
        """

        file_path = '/'.join(label_path.split('/')[3:])
        file_path = '/'.join([self.dir_path, file_path])
        dir_path = '/'.join(file_path.split('/')[:-1])

        os.makedirs(dir_path, exist_ok=True)
        if not os.path.exists(file_path):
            # ファイルが存在しない場合
            Utils.download_file_to_dir(label_path,dir_path)
            time.sleep(2)

        return file_path

    def __get_file_path(self, label_uri:str) -> str:
        """
        ラベルURIに基づいてファイルパスを取得します。

        Args:
            label_uri (str): ラベルのURI。

        Returns:
            str: ファイルパス。
        """

        file_path = ""
        if "http" in label_uri:
            file_path = self.__get_global_file_path(label_uri)
        else:
            file_path = self.__get_local_file_path(label_uri)

        return file_path

    def __get_xlink_label(self, file_path:str, xlink_name:str) -> str:
        """
        指定されたファイル内でxlink:name属性が一致するラベルを検索します。

        Args:
            file_path (str): 検索対象のファイルパス。
            xlink_name (str): 検索するxlink:name属性の値。

        Returns:
            str: 見つかったラベル。
        """

        label_parser = XbrlParserController.xml_label_parser(file_path)
        loc_df = label_parser.link_locs
        loc_df = loc_df.query(f"xlink_href == '{xlink_name}'")
        return loc_df.iloc[0]['xlink_label']

    def __get_arc_to_label(self, file_path:str, xlink_label:str) -> list:
        """
        指定されたラベルからアークを通じて関連付けられているラベルのリストを取得します。

        Args:
            file_path (str): ファイルパス。
            xlink_label (str): xlink:label属性の値。

        Returns:
            list: 関連付けられているラベルのリスト。
        """

        label_parser = XbrlParserController.xml_label_parser(file_path)
        arc_df = label_parser.link_label_arcs
        arc_df = arc_df.query(f"xlink_from == '{xlink_label}'")
        return arc_df['xlink_to'].to_list()

    def __get_label_list(self, file_path:str, arc_list:list) -> list:
        """
        指定されたアークリストに基づいてラベルのリストを取得します。

        Args:
            file_path (str): ファイルパス。
            arc_list (list): アークのリスト。

        Returns:
            list: ラベルのテキストのリスト。
        """

        label_parser = XbrlParserController.xml_label_parser(file_path)
        label_df = label_parser.link_labels
        label_df = label_df[label_df['xlink_label'].isin(arc_list)]
        # target_row = label_df.query("xlink_role == 'http://www.xbrl.org/2003/role/label'")
        label_text = label_df['text'].to_list()

        return label_text

    def get_link_label(self, xlink_name: str, role_number:int) -> str | None:
        """
        指定されたxlink:nameと役割番号に基づいてラベルを取得します。

        Args:
            xlink_name (str): xlink:name属性の値。
            role_number (int): 役割番号。

        Returns:
            str | None: 見つかったラベル、またはrole_numberが無効な場合はNone。
        """

        # 名前空間を取得する
        name_space = xlink_name.split('_')[0]
        # ラベルファイルのパスを取得する
        label_uri = self.__get_xlink_href(name_space)
        # ローカルラベルとグローバルラベルで処理を分岐
        file_path = self.__get_file_path(label_uri)

        xlink_label = self.__get_xlink_label(file_path,xlink_name)
        arc_list = self.__get_arc_to_label(file_path, xlink_label)
        labels = self.__get_label_list(file_path, arc_list)

        try:
          return labels[role_number]
        except IndexError as e:
          print('role_numberが存在しません。')
          return None

if __name__ == '__main__':
    zip_path:str = "/Users/user/Vscode/python/PyXBRLTools/doc/dummy.zip"
    extra_dir:str = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir"
    url = "http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab.xml"
    # Utils.extract_zip(zip_path,extra_dir)

    lm = LabelManager(extra_dir)
    g_label_name = "jppfs_cor_IncreaseDecreaseInProvisionForDirectorsRetirementBenefitsOpeCF"
    l_label_name = "tse-acedjpfr-57210_LossOnValuationOfStocksOfSubsidiariesOpeCF"
    label_str = lm.get_link_label(g_label_name, 0)
    print(label_str)
    # Utils.initialize_directory(extra_dir)