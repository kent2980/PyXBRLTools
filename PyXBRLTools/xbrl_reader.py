from xbrl_manager.xbrl_label_manager import XbrlLabelManager
from xbrl_manager.xbrl_link_manager import XbrlLinkManager, XbrlLinkType
from xbrl_manager.ixbrl_manager import IxbrlManager
from xbrl_model.ixbrl_models import IxbrlModel
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

        # XBRLモデルをインスタンス化
        self.__ixbrl_model = IxbrlModel(self.__xbrl_directory_path, self.__load_label_directory)

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

        dict = self.__ixbrl_model.ix_non_fraction

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
        dict = self.__ixbrl_model.ix_non_numeric
        print("********ix_non_numerics********************************************")
        print(dict)
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