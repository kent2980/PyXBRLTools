import os
import pandas as pd
from abc import ABC, abstractmethod
import time
import logging
from log.py_xbrl_tools_loging import PyXBRLToolsLogging
from xbrl_parser.xbrl_roles_definitions import XbrlRole
from xbrl_parser.xbrl_parser_controller import XbrlParserController
from utils.utils import Utils
from typing import Type

class BaseLabelManager(ABC):
    """XBRLラベルの基底クラスです。
    XBRLのelementからラベルを取得するクラスです。
    """
    def __init__(self, dir_path:str):
        """BaseLabelManagerのコンストラクタです。
        Args:
            dir_path (str): ディレクトリのパス。
        """
        self.__dir_path = dir_path
        self.label_parser = XbrlParserController.xml_label_parser()
        self._element_names = []

        # ログ設定
        class_name = self.__class__.__name__
        print(class_name)
        self.logger = PyXBRLToolsLogging(log_level=logging.DEBUG)
        self.logger.set_log_file(f'Log/{class_name}.log')

        # ログを出力
        self.logger.logger.info(f"{class_name}を初期化しました。")
        self.logger.logger.info(f"dir_path(入力フォルダ)を設定: {dir_path}")

    @property
    def dir_path(self):
        """ディレクトリのパスを取得します。
        Returns:
            str: ディレクトリのパス。
        """
        return self.__dir_path

    @dir_path.setter
    def dir_path(self, dir_path:str):
        """ディレクトリのパスを設定します。
        Args:
            dir_path (str): ディレクトリのパス。
        """
        self.__dir_path = dir_path
        self._element_names = []

        # ログを出力
        self.logger.logger.info(f"dir_path(入力フォルダ)を変更: {dir_path}")

    @abstractmethod
    def link_label(self,element_name:str, index:int = 0) -> str:
        """ラベルを取得します。
        Args:
            element_name (str): 要素名。
            index (int): ラベルのインデックス。
        Returns:
            str: ラベル。
        """
        pass

    @abstractmethod
    def link_label_itertor(self, element_names:list, xbrl_role: Type[XbrlRole] = 0):
        """ラベルをイテレータで取得します。
        """
        pass

    @abstractmethod
    def locs_table_df(self, element_names:list) -> pd.DataFrame:
        """locsテーブルを取得します。

        args:
            element_names (list): Elementのリスト。

        Returns:
            pd.DataFrame: locsテーブル。
        """
        pass

    @abstractmethod
    def arcs_table_df(self, element_names:list) -> pd.DataFrame:
        """arcsテーブルを取得します。

        args:
            element_names (list): Elementのリスト。

        Returns:
            pd.DataFrame: arcsテーブル。
        """
        pass

    @abstractmethod
    def labels_table_df(self, element_names:list) -> pd.DataFrame:
        """labelsテーブルを取得します。

        args:
            element_names (list): Elementのリスト。

        Returns:
            pd.DataFrame: labelsテーブル。
        """
        pass

class LabelManager(BaseLabelManager):
    """XBRLラベルのクラスです。
    """

    def __get_lab_path(self, name_space:str) -> str:
        """ ラベルファイルのパスを取得します。

        args:
            name_space (str): 名前空間。

        returns:
            str: ラベルファイルのパス。

        example:
            >>> __get_lab_path("jpcrp")
            "http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab.xml"
        """

        # ディレクトリからスキーマファイル一覧を再帰的に検索して取得
        for root, dirs, files in os.walk(self.dir_path):
            # ファイル一覧を取得
            for file in files:
                # xsdファイルの場合
                if file.endswith('.xsd'):
                    schema_file_path = os.path.join(root, file)
                    schema = XbrlParserController.xml_schema_parser(schema_file_path)
                    link_base_refs = schema.get_link_base_refs()
                    # name_spaceに一致するリンクベース参照を取得
                    link_base_ref = link_base_refs[link_base_refs['xlink_href'].str.contains(name_space)
                                & (link_base_refs['xlink_role'] == "http://www.xbrl.org/2003/role/labelLinkbaseRef")
                                & (link_base_refs['xlink_href'].str.endswith('lab.xml'))]
                    # link_base_refに要素がある場合
                    if not link_base_ref.empty:
                        lab_path = link_base_ref.iloc[0]['xlink_href']
                        return lab_path

    def __get_local_file_path(self, label_path:str) -> str:
        """
        ローカルファイルシステム上でのラベルファイルのパスを取得します。

        Args:
            label_path (str): ラベルファイルのパス。

        Returns:
            str: ファイルのフルパス。

        example:
            >>> __get_local_file_path("tse-acedjpfr-57210-2024-03-31-01-2024-05-13-lab.xml")
            "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab.xml"
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

        example:
            >>> __get_global_file_path("http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab.xml")
            "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab.xml"
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

    def __get_label_dfs(self, lab_paths:list) -> pd.DataFrame:
        """ラベルファイルのDataFrameを取得します。

        Args:
            lab_paths (list): ラベルファイルのパスのリスト。

        Returns:
            pd.DataFrame: ラベルファイルのDataFrame。

        example:
            >>> df = __get_label_dfs(["http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab.xml"])
            pd.DataFrame
            print(df)
            output:
            |   | xlink_href | xlink_label | xlink_from | xlink_to | text |
            |---|------------|-------------|------------|----------|------|
            | 0 | jpcrp_cor_EquityClassOfShares | jpcrp_cor_EquityClassOfShares | jpcrp_cor_EquityClassOfShares | jpcrp_cor_EquityClassOfShares | 株式の種類 |
            | 1 | jpcrp_cor_EquityClassOfShares | jpcrp_cor_EquityClassOfShares | jpcrp_cor_EquityClassOfShares | jpcrp_cor_EquityClassOfShares | 株式の種類 |
        """

        loc_df = pd.DataFrame()
        arc_df = pd.DataFrame()
        label_df = pd.DataFrame()

        for lab_path in lab_paths:
            # ラベルファイルをパース
            self.label_parser.file_path = lab_path

            # locラベルを取得
            loc_df2 = self.label_parser.get_link_locs()
            # loclabelsにloc_labelを追加しインデックスを振り直す
            loc_df = pd.concat([loc_df, loc_df2], ignore_index=True)

            # arcラベルを取得
            arc_df2 = self.label_parser.get_link_label_arcs()
            arc_df = pd.concat([arc_df, arc_df2], ignore_index=True)

            # labelラベルを取得
            label_df2 = self.label_parser.get_link_labels()
            label_df = pd.concat([label_df, label_df2], ignore_index=True)

        # loc_dfの'xlink_label'カラムとarc_dfの'xlink_from'カラムを結合
        result_df = pd.merge(loc_df, arc_df, left_on='xlink_label', right_on='xlink_from', how='left')
        # loc_dfの'xlink_label'カラムとlabel_dfの'xlink_label'カラムを結合
        result_df = pd.merge(result_df, label_df, left_on='xlink_to', right_on='id', how='left')

        return result_df

    def __get_lab_paths(self, element_names:list) -> list:
        lab_paths = []

        for element_name in element_names:

            # 名前空間と要素ラベルを取得
            name_space = element_name.split('_')[0]
            # ラベルファイルのパスを取得
            lab_path = self.__get_lab_path(name_space)

            # lab.xmlのローカルパスを取得
            if "http" in lab_path:
                lab_path = self.__get_global_file_path(lab_path)
            else:
                lab_path = self.__get_local_file_path(lab_path)

            lab_paths.append(lab_path)

        # lab_pathsの重複を削除
        lab_paths = list(set(lab_paths))

        return lab_paths


    def link_label(self, element_name:str, xbrl_role: str | None = None) -> str:
        """ラベルを取得します。

        Args:
            element_name (str): 要素名。
            xbrl_role (Type[XbrlRole]): ラベルのインデックス。(default: 'http://www.xbrl.org/2003/role/label')

        Returns:
            str: ラベル。

        example:
            >>> link_label("jppfs_cor_EquityClassOfShares", 1)
            "株式の種類"
        """

        # 名前空間と要素ラベルを取得
        name_space = element_name.split('_')[0]
        # ラベルファイルのパスを取得
        lab_path = self.__get_lab_path(name_space)

        # lab.xmlのローカルパスを取得
        if "http" in lab_path:
            lab_path = self.__get_global_file_path(lab_path)
        else:
            lab_path = self.__get_local_file_path(lab_path)

        result_df = self.__get_label_dfs([lab_path])

        # loc_dfの'xlink_href'カラムとelement_nameが一致する行を取得
        loc_df2 = result_df[result_df['xlink_href'] == element_name]
        # loc_df2の指定したxbrl_roleの行を取得, xbrl_roleが指定されていない場合は全ての行を取得
        if xbrl_role is not None:
            loc_df2 = loc_df2.query(f'xlink_role == "{xbrl_role}"')

        # 例外処理
        try:
            # loc_df2の指定したインデックスの行を取得,要素がない場合はエラーを発生して例外処理
            loc_df2 = loc_df2.iloc[0]
        except IndexError:
            # ログファイルにエラーメッセージを出力
            self.logger.logger.error(f"要素名'{element_name}'が見つかりませんでした。")

        # ラベル名を取得
        label_ja_label = loc_df2['label']

        return label_ja_label

    def link_label_itertor(self, element_names:list, xbrl_role: str | None = None):
        """_summary_

        Args:
            element_names (list): Elementのリスト
            xbrl_role (Type[XbrlRole]): ラベルのインデックス。(default: 'http://www.xbrl.org/2003/role/label')

        yields:
            tuple: element_name, label_ja_label

        example:
            >>> link_label_itertor(["jppfs_cor_EquityClassOfShares", "jppfs_cor_EquityClassOfShares"], 1)
            ("jppfs_cor_EquityClassOfShares", "株式の種類")
            ("jppfs_cor_EquityClassOfShares", "株式の種類")
        """

        # lab_pathsの重複を削除
        lab_paths = self.__get_lab_paths(element_names)

        result_df = self.__get_label_dfs(lab_paths)

        for element_name in element_names:
            # loc_dfの'xlink_href'カラムとelement_nameが一致する行を取得
            loc_df2 = result_df[result_df['xlink_href'] == element_name]
            # loc_df2の指定したxbrl_roleの行を取得, xbrl_roleが指定されていない場合は全ての行を取得
            if xbrl_role is not None:
                loc_df2 = loc_df2.query(f'xlink_role == "{xbrl_role}"')

            # 例外処理
            try:
                # loc_df2の指定したインデックスの行を取得,要素がない場合はエラーを発生して例外処理
                loc_df2 = loc_df2.iloc[0]
            except IndexError:
                # ログファイルにエラーメッセージを出力
                self.logger.logger.error(f"要素名'{element_name}'が見つかりませんでした。")
                # エラーが発生したら次の要素に移動
                continue

            # ラベル名を取得
            label_ja_label = loc_df2['label']

            yield element_name, label_ja_label

    def locs_table_df(self, element_names:list) -> pd.DataFrame:
        lab_paths = self.__get_lab_paths(element_names)

        loc_df = pd.DataFrame()
        for lab_path in lab_paths:
            # ラベルファイルをパース
            self.label_parser.file_path = lab_path

            # locラベルを取得
            loc_df2 = self.label_parser.get_link_locs()
            # loclabelsにloc_labelを追加しインデックスを振り直す
            loc_df = pd.concat([loc_df, loc_df2], ignore_index=True)

        return loc_df

    def arcs_table_df(self, element_names:list) -> pd.DataFrame:
        lab_paths = self.__get_lab_paths(element_names)

        arc_df = None
        for lab_path in lab_paths:
            # ラベルファイルをパース
            self.label_parser.file_path = lab_path

            # arcラベルを取得
            arc_df2 = self.label_parser.get_link_label_arcs()
            # arc_dfにarc_labelを追加しインデックスを振り直す,arc_df2が空の場合は次の要素に移動
            if not arc_df is None:
                arc_df = pd.concat([arc_df, arc_df2], ignore_index=True)
            else:
                arc_df = arc_df2

        return arc_df

    def labels_table_df(self, element_names:list, xbrl_role: str | None = None) -> pd.DataFrame:
        lab_paths = self.__get_lab_paths(element_names)

        label_df = pd.DataFrame()
        for lab_path in lab_paths:
            # ラベルファイルをパース
            self.label_parser.file_path = lab_path

            # labelラベルを取得
            label_df2 = self.label_parser.get_link_labels()
            label_df = pd.concat([label_df, label_df2], ignore_index=True)

        if xbrl_role is not None:
            label_df = label_df.query(f'xlink_role == "{xbrl_role}"')

        return label_df

    def role_refs_table_df(self, element_names:list) -> pd.DataFrame:
        lab_paths = self.__get_lab_paths(element_names)

        role_ref_df = pd.DataFrame()
        for lab_path in lab_paths:
            # ラベルファイルをパース
            self.label_parser.file_path = lab_path

            # roleRefラベルを取得
            role_ref_df2 = self.label_parser.get_role_refs()
            role_ref_df = pd.concat([role_ref_df, role_ref_df2], ignore_index=True)

        return role_ref_df