from xbrl_manager.xbrl_label_manager import XbrlLabelManager
from xbrl_manager.xbrl_link_manager import XbrlLinkManager, XbrlLinkType
from xbrl_manager.ixbrl_manager import IxbrlManager
import zipfile
import shutil
import os
import time
from db_connector.postgre_sql_connector import PostgreSqlConnector

class XbrlReader:
    """ XBRLファイルを読み込むクラスです。

    Args:
        xbrl_zip_path (str): XBRLファイルのZIPファイルのパス
        xbrl_directory_path (str): XBRLファイルを解凍するディレクトリのパス
        load_label_directory (str): グローバルラベルファイルをロードするディレクトリのパス

    Properties:
        xbrl_zip_path (str): XBRLファイルのZIPファイルのパス
        xbrl_directory_path (str): XBRLファイルを解凍するディレクトリのパス
        load_label_directory (str): グローバルラベルファイルをロードするディレクトリのパス

    Methods:
        get_ix_non_fractions: iXBRLファイルの非分数を取得するメソッド
        get_ix_non_numerics: iXBRLファイルの非数値を取得するメソッド

    Examples:
        >>> xbrl_zip_path = '/Users/user/Vscode/python/PyXBRLTools/doc/081220240327560965.zip'
        >>> xbrl_direrctory_path = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRL'
        >>> load_xbrl_directory_path = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/labels'

        >>> xbrl_read = XbrlRead(xbrl_zip_path, xbrl_direrctory_path, load_xbrl_directory_path)

        >>> ix_non_fractions = xbrl_read.get_ix_non_fractions()
        >>> for key, value in ix_non_fractions.items():
        >>>     print(f'{key}: {value}')

        >>> ix_non_numerics = xbrl_read.get_ix_non_numerics()
        >>> for key, value in ix_non_numerics.items():
        >>>     print(f'{key}: {value}')
    """
    def __init__(self, xbrl_zip_path, xbrl_directory_path, load_label_directory):
        """ コンストラクタ

        Args:
            xbrl_zip_path (str): XBRLファイルのZIPファイルのパス
            xbrl_directory_path (str): XBRLファイルを解凍するディレクトリのパス
            load_label_directory (str): グローバルラベルファイルをロードするディレクトリのパス

        Examples:
            >>> xbrl_zip_path = '/Users/user/Vscode/python/PyXBRLTools/doc/081220240327560965.zip'
            >>> xbrl_direrctory_path = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRL'
            >>> load_xbrl_directory_path = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/labels'

            >>> xbrl_read = XbrlRead(xbrl_zip_path, xbrl_direrctory_path, load_xbrl_directory_path)
        """

        # ZIPファイルのパスを設定
        self.__xbrl_zip_path = xbrl_zip_path
        # zipファイルの名前を取得
        self.__xbrl_zip_filename = xbrl_zip_path.split('/')[-1].split('.')[0]
        # ZIPファイルを解凍するディレクトリのパスを設定
        self.__xbrl_directory_path = f"{xbrl_directory_path}/{self.__xbrl_zip_filename}"
        # グローバルラベルファイルをロードするディレクトリのパスを設定
        self.__load_label_directory = load_label_directory
        # zipファイルを解凍
        zipfile.ZipFile(xbrl_zip_path).extractall(self.__xbrl_directory_path)

        # iXBRLマネージャーのインスタンスを作成
        self.__ixbrl_manager = IxbrlManager(self.__xbrl_directory_path)
        # IXBRLラベルマネージャーのインスタンスを作成
        self.__label_manager = XbrlLabelManager(self.__xbrl_directory_path, self.__load_label_directory)
        # IXBRLリンクマネージャーのインスタンスを作成
        self.__link_manager = XbrlLinkManager(self.__xbrl_directory_path, XbrlLinkType.CAL)

        # ラベルLocsを取得
        self.__label_locs = self.__label_manager.get_label_locs()
        # ラベルArcsを取得
        self.__label_arcs = self.__label_manager.get_label_arcs()
        # ラベルを取得
        self.__labels = self.__label_manager.get_labels()

        # リンクlocsを取得
        self.__cal_link_locs = self.__link_manager.get_link_locs()
        # リンクArcsを取得
        self.__cal_link_arcs = self.__link_manager.get_link_arcs()

        # link_typeをDEFに変更
        self.__link_manager.link_type = XbrlLinkType.DEF
        # リンクlocsを取得
        self.__def_link_locs = self.__link_manager.get_link_locs()
        # リンクArcsを取得
        self.__def_link_arcs = self.__link_manager.get_link_arcs()

        # link_typeをPREに変更
        self.__link_manager.link_type = XbrlLinkType.PRE
        # リンクlocsを取得
        self.__pre_link_locs = self.__link_manager.get_link_locs()
        # リンクArcsを取得
        self.__pre_link_arcs = self.__link_manager.get_link_arcs()

    def __del__(self):
        """ デストラクタ """
        # 解凍したファイルを削除
        if os.path.exists(self.__xbrl_directory_path):
            shutil.rmtree(self.__xbrl_directory_path)

    @property
    def xbrl_zip_path(self):
        """ XBRLファイルのZIPファイルのパスを取得するプロパティです。"""
        return self.__xbrl_zip_path

    @property
    def xbrl_directory_path(self):
        """ XBRLファイルを解凍するディレクトリのパスを取得するプロパティです。"""
        return self.__xbrl_directory_path

    @property
    def load_label_directory(self):
        """ グローバルラベルファイルをロードするディレクトリのパスを取得するプロパティです。"""
        return self.__load_label_directory

    def get_ix_non_fractions(self):
        """
        iXBRLファイルの非分数を取得するメソッドです。

        Returns:
            dict: iXBRLファイルの非分数を格納した辞書

        Examples:
            dict['ix_non_fractions']: iXBRLファイルの非分数
            dict['ix_non_fractions_label_arcs']: ラベルArcs
            dict['ix_non_fractions_label_locs']: ラベルLocs
            dict['ix_non_fractions_labels']: ラベル
            dict['ix_non_fractions_cal_link_locs']: CALリンクLocs
            dict['ix_non_fractions_cal_link_arcs']: CALリンクArcs
            dict['ix_non_fractions_def_link_arcs']: DEFリンクArcs
            dict['ix_non_fractions_pre_link_arcs']: PREリンクArcs
            dict['ix_non_fractions_def_link_locs']: DEFリンクLocs
            dict['ix_non_fractions_pre_link_locs']: PREリンクLocs
        """
        dict = {}
        # ix_non_fractionsを取得
        ix_non_fractions = self.__ixbrl_manager.ix_non_fractions
        # ix_non_fractionsのnameを取得
        ix_non_fractions_name = list(set(ix_non_fractions['name'].to_list()))

        # label_locsを取得
        label_locs = self.__label_locs[self.__label_locs['xlink_href'].isin(ix_non_fractions_name)]
        # label_locsのxlink_labelを取得
        label_locs_xlink_label = list(set(label_locs['xlink_label'].to_list()))
        # label_arcsを取得
        label_arcs = self.__label_arcs[self.__label_arcs['xlink_from'].isin(label_locs_xlink_label)]
        # label_arcsのxlink_toを取得
        label_arcs_xlink_to = list(set(label_arcs['xlink_to'].to_list()))
        # labelを取得
        labels = self.__labels[self.__labels['xlink_label'].isin(label_arcs_xlink_to)]

        # cal_link_locsを取得
        cal_link_locs = self.__cal_link_locs[self.__cal_link_locs['xlink_href'].isin(ix_non_fractions_name)]
        # cal_link_locsのxlink_labelを取得
        cal_link_locs_xlink_label = list(set(cal_link_locs['xlink_label'].to_list()))
        # cal_link_arcsを取得
        cal_link_arcs = self.__cal_link_arcs[self.__cal_link_arcs['xlink_to'].isin(cal_link_locs_xlink_label)]

        # def_link_locsを取得
        def_link_locs = self.__def_link_locs[self.__def_link_locs['xlink_href'].isin(ix_non_fractions_name)]
        # def_link_locsのxlink_labelを取得
        def_link_locs_xlink_label = list(set(def_link_locs['xlink_label'].to_list()))
        # def_link_arcsを取得
        def_link_arcs = self.__def_link_arcs[self.__def_link_arcs['xlink_to'].isin(def_link_locs_xlink_label)]

        # pre_link_locsを取得
        pre_link_locs = self.__pre_link_locs[self.__pre_link_locs['xlink_href'].isin(ix_non_fractions_name)]
        # pre_link_locsのxlink_labelを取得
        pre_link_locs_xlink_label = list(set(pre_link_locs['xlink_label'].to_list()))
        # pre_link_arcsを取得
        pre_link_arcs = self.__pre_link_arcs[self.__pre_link_arcs['xlink_to'].isin(pre_link_locs_xlink_label)]

        # 辞書に各値を格納します
        dict['ix_non_fractions'] = ix_non_fractions
        dict['ix_non_fractions_label_arcs'] = label_arcs
        dict['ix_non_fractions_label_locs'] = label_locs
        dict['ix_non_fractions_labels'] = labels
        dict['ix_non_fractions_cal_link_locs'] = cal_link_locs
        dict['ix_non_fractions_cal_link_arcs'] = cal_link_arcs
        dict['ix_non_fractions_def_link_locs'] = def_link_locs
        dict['ix_non_fractions_def_link_arcs'] = def_link_arcs
        dict['ix_non_fractions_pre_link_locs'] = pre_link_locs
        dict['ix_non_fractions_pre_link_arcs'] = pre_link_arcs

        # ix_non_fractions, label_arcs, label_locs, labels, cal_link_locs, cal_link_arcs, def_link_arcs, pre_link_arcs, def_link_locs, pre_link_locsを返す
        return dict

    def get_ix_non_numerics(self):
        """
        iXBRLファイルの非数値を取得するメソッドです。

        Returns:
            dict: iXBRLファイルの非数値を格納した辞書

        Examples:
            dict['ix_non_numerics']: iXBRLファイルの非数値
            dict['ix_non_numerics_label_arcs']: ラベルArcs
            dict['ix_non_numerics_label_locs']: ラベルLocs
            dict['ix_non_numerics_labels']: ラベル
        """
        dict = {}
        # ix_non_numericsを取得
        ix_non_numerics = self.__ixbrl_manager.ix_non_numerics
        # ix_non_numericsのnameを取得
        ix_non_numerics_name = list(set(ix_non_numerics['name'].to_list()))

        # label_locsを取得
        label_locs = self.__label_locs[self.__label_locs['xlink_href'].isin(ix_non_numerics_name)]
        # label_locsのxlink_labelを取得
        label_locs_xlink_label = list(set(label_locs['xlink_label'].to_list()))
        # label_arcsを取得
        label_arcs = self.__label_arcs[self.__label_arcs['xlink_from'].isin(label_locs_xlink_label)]
        # label_arcsのxlink_toを取得
        label_arcs_xlink_to = list(set(label_arcs['xlink_to'].to_list()))
        # labelを取得
        labels = self.__labels[self.__labels['xlink_label'].isin(label_arcs_xlink_to)]

        # 辞書に各値を格納します
        dict['ix_non_numerics'] = ix_non_numerics
        dict['ix_non_numerics_label_arcs'] = label_arcs
        dict['ix_non_numerics_label_locs'] = label_locs
        dict['ix_non_numerics_labels'] = labels

        # ix_non_numerics, label_arcs, label_locs, labelsを返す
        return dict


if __name__ == '__main__':
    # 処理時間を計測
    start = time.time()

    xbrl_zip_path = '/Users/user/Vscode/python/PyXBRLTools/doc/081220240327560965.zip'
    xbrl_direrctory_path = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRL'
    load_xbrl_directory_path = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/labels'

    xbrl_read = XbrlReader(xbrl_zip_path, xbrl_direrctory_path, load_xbrl_directory_path)

    connector = PostgreSqlConnector("localhost", 5432, "fsstock", "postgres", "full6839")
    connector.connect()

    ix_non_fractions = xbrl_read.get_ix_non_fractions()
    for key, value in ix_non_fractions.items():
        print(f'{key}: {value}')
        connector.create_table_from_df(key, value)

    ix_non_numerics = xbrl_read.get_ix_non_numerics()
    for key, value in ix_non_numerics.items():
        print(f'{key}: {value}')
        connector.create_table_from_df(key, value)

    connector.disconnect()

    # 処理時間を表示
    elapsed_time = time.time() - start

    print(f"処理時間：{elapsed_time}秒")