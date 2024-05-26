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

    def __init__(self, dir_path:str, xlink_name:str):
        self.__dir_path = dir_path
        self.__xlink_name = xlink_name

    @property
    def dir_path(self):
        """ディレクトリのパスを取得します。"""
        return self.__dir_path

    @dir_path.setter
    def dir_path(self, dir_path:str):
        self.__dir_path = dir_path

    @property
    def xlink_name(self):
        return self.__xlink_name

    @xlink_name.setter
    def xlink_name(self, xlink_name:str):
        self.__xlink_name = xlink_name

    @abstractmethod
    def get_link_label(self, xlink_href:str) -> str | None:
        """
        xlink:href属性に基づいてラベルを取得するための抽象メソッドです。

        Args:
            xlink_href (str): 取得したいラベルのxlink:href属性。

        Returns:
            str | None: 見つかったラベル、またはrole_numberが無効な場合はNone。
        """
        pass

    @abstractmethod
    def get_locs_table_df(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_arcs_table_df(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_labels_table_df(self) -> pd.DataFrame:
        pass

class LabelManager(BaseLabelManager):
    """
    XBRLラベルを管理するためのクラスです。

    BaseLabelManager を継承しています。
    """

    def __init__(self, dir_path: str, xlink_name: str):
        super().__init__(dir_path, xlink_name)
        self.__file_path = self.__get_file_path(xlink_name)
        self.__label_parser = XbrlParserController.xml_label_parser(self.__file_path)

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

    def __get_file_path(self, xlink_name:str) -> str:
        """
        ラベルURIに基づいてファイルパスを取得します。

        Args:
            label_uri (str): ラベルのURI。

        Returns:
            str: ファイルパス。
        """

        # 名前空間を取得する
        name_space = xlink_name.split('_')[0]
        # ラベルファイルのパスを取得する
        label_uri = self.__get_xlink_href(name_space)

        file_path = ""
        if "http" in label_uri:
            file_path = self.__get_global_file_path(label_uri)
        else:
            file_path = self.__get_local_file_path(label_uri)

        return file_path

    def __get_loc_xlink_label_df(self, xlink_name:str) -> pd.DataFrame:
        """
        指定されたファイル内でxlink:name属性が一致するラベルを検索します。

        Args:
            file_path (str): 検索対象のファイルパス。
            xlink_name (str): 検索するxlink:name属性の値。

        Returns:
            str: 見つかったラベル。
        """

        loc_df = self.__label_parser.link_locs
        loc_df = loc_df.query(f"xlink_href == '{xlink_name}'")

        return loc_df

    def __get_arc_to_df(self, xlink_label:str) -> pd.DataFrame:
        """
        指定されたラベルからアークを通じて関連付けられているラベルのリストを取得します。

        Args:
            file_path (str): ファイルパス。
            xlink_label (str): xlink:label属性の値。

        Returns:
            list: 関連付けられているラベルのリスト。
        """

        arc_df = self.__label_parser.link_label_arcs
        arc_df = arc_df.query(f"xlink_from == '{xlink_label}'")

        return arc_df

    def __get_label_df(self, arc_list:list) -> pd.DataFrame:
        """
        指定されたアークリストに基づいてラベルのリストを取得します。

        Args:
            file_path (str): ファイルパス。
            arc_list (list): アークのリスト。

        Returns:
            list: ラベルのテキストのリスト。
        """

        label_df = self.__label_parser.link_labels
        label_df = label_df[label_df['xlink_label'].isin(arc_list)]

        return label_df

    def get_link_label(self, role_number:int) -> str | None:
        """
        指定されたxlink:nameと役割番号に基づいてラベルを取得します。

        Args:
            xlink_name (str): xlink:name属性の値。
            role_number (int): 役割番号。

        Returns:
            str | None: 見つかったラベル、またはrole_numberが無効な場合はNone。
        """

        # ローカルラベルとグローバルラベルで処理を分岐
        # file_path = self.__get_file_path(xlink_name)
        # locタグからxlink_labelを取得する
        xlink_label = self.__get_loc_xlink_label_df(self.xlink_name).iloc[0]['xlink_label']
        # arcタグからxlink_toのリストを取得する
        arc_list = self.__get_arc_to_df(xlink_label)['xlink_to'].to_list()
        # 勘定ラベルのリストを取得する
        labels = self.__get_label_df(arc_list)['text'].to_list()

        try:
            return labels[role_number]
        except IndexError as e:
            print('role_numberが存在しません。')
            return None

    def get_locs_table_df(self) -> pd.DataFrame:

        # file_path = self.__get_file_path(xlink_name)

        xlink_label_df = self.__get_loc_xlink_label_df(self.xlink_name)

        return xlink_label_df

    def get_arcs_table_df(self) -> pd.DataFrame:

        # locタグからxlink_labelを取得する
        xlink_label = self.__get_loc_xlink_label_df(self.xlink_name).iloc[0]['xlink_label']

        arcs_df = self.__get_arc_to_df(xlink_label)

        return arcs_df

    def get_labels_table_df(self) -> pd.DataFrame:

        # locタグからxlink_labelを取得する
        xlink_label = self.__get_loc_xlink_label_df(self.xlink_name).iloc[0]['xlink_label']
        # arcタグからxlink_toのリストを取得する
        arc_list = self.__get_arc_to_df(xlink_label)['xlink_to'].to_list()
        # 勘定ラベルのリストを取得する
        labels_df = self.__get_label_df(arc_list)

        return labels_df

if __name__ == '__main__':
    zip_path:str = "/Users/user/Vscode/python/PyXBRLTools/doc/dummy.zip"
    extra_dir:str = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir"
    url = "http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab.xml"
    # Utils.extract_zip(zip_path,extra_dir)

    g_label_name = "jppfs_cor_IncreaseDecreaseInProvisionForDirectorsRetirementBenefitsOpeCF"
    l_label_name = "tse-acedjpfr-57210_LossOnValuationOfStocksOfSubsidiariesOpeCF"
    lm = LabelManager(extra_dir, g_label_name)
    label_str = lm.get_link_label(0)
    print(label_str)
    print(lm.get_locs_table_df())
    print(lm.get_arcs_table_df())
    print(lm.get_labels_table_df())
    # Utils.initialize_directory(extra_dir)