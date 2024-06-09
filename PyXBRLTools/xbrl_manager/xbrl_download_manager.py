import os
import requests
from xbrl_parser.xml_schema_parser import XmlSchemaParser
import time

class XBRLDownloadManager:
    """ XBRLファイルをダウンロードするクラスです。

    Attributes:
        Xbrl_save_dir (str): XBRLファイルの保存ディレクトリ

    Properties:
        Xbrl_save_dir (str): XBRLファイルの保存ディレクトリ

    Methods:
        __init__: コンストラクタ
        __get_xbrl_files: XBRLスキーマファイルからXBRLファイルのリストを取得するメソッド
        load_xbrl_files_from_schema: XBRLファイルをスキーマファイルからダウンロードするメソッド
        load_xbrl_files_from_list: XBRLファイルをリストからダウンロードするメソッド

    Examples:
        >>> xbrl_download_manager = XBRLDownloadManager(Xbrl_save_dir)
        >>> for xbrl_file_path in xbrl_download_manager.load_xbrl_files_from_schema(xbrl_schema_path):
        >>>     print(xbrl_file_path)
        output:
        [
        '/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab.xml',
        '/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab-en.xml',
        ]
    """

    def __init__(self, Xbrl_save_dir):
        """ コンストラクタ

        Args:
            xbrl_schema_path (str): XBRLスキーマファイルのパス
            Xbrl_save_dir (str): XBRLファイルの保存ディレクトリ
        """
        self.__Xbrl_save_dir = Xbrl_save_dir

    @property
    def Xbrl_save_dir(self):
        """ XBRLファイルの保存ディレクトリを取得します。"""
        return self.__Xbrl_save_dir

    @Xbrl_save_dir.setter
    def Xbrl_save_dir(self, Xbrl_save_dir):
        """ XBRLファイルの保存ディレクトリを設定します。

        Args:
            Xbrl_save_dir (str): XBRLファイルの保存ディレクトリ
        """
        self.__Xbrl_save_dir = Xbrl_save_dir

    def __get_xbrl_files(self, xbrl_schema_path):
        """ XBRLスキーマファイルからXBRLファイルのリストを取得します。 """
        # XBRLスキーマファイルを読み込みます。
        parser = XmlSchemaParser(xbrl_schema_path)
        # ファイルのリストを取得します。
        xbrl_files_df = parser.link_base_refs
        # ファイルリストのDataFrameからxlink_hrefカラムにhttpを含むものを抽出します。
        xbrl_files_df = xbrl_files_df[xbrl_files_df['xlink_href'].str.contains('http')]
        # ファイルリストのDataFrameからxlink_hrefカラムの値をリストに変換します。
        xbrl_files = xbrl_files_df['xlink_href'].tolist()

        return xbrl_files

    def load_xbrl_files_from_schema(self, xbrl_schema_path, sleep_time = 2) -> list[str]:
        """ XBRLファイルをスキーマファイルからダウンロードします。
            保存したXBRLファイルのローカルパスのリストを返します。
            サーバーへの負荷を考慮して、ダウンロード間隔を設定できます。
            ダウンロード間隔の初期設定は2秒です。

        Args:
            xbrl_schema_path (str): XBRLスキーマファイルのパス
            sleep_time (int): ダウンロード間隔の秒数

        Returns:
            list: XBRLファイルのローカルパスのリスト

        Raises:
            ValueError: 待機時間が2秒未満の場合

        Examples:
            >>> xbrl_download_manager = XBRLDownloadManager(xbrl_schema_path, Xbrl_save_dir)
            >>> for xbrl_file_path in xbrl_download_manager.download_xbrl_files():
            >>>     print(xbrl_file_path)
            output:
            [
            '/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab.xml',
            '/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab-en.xml',
            ]
        """
        if sleep_time < 2:
            raise ValueError('待機時間は2秒以上に設定してください。')

        lists = []

        xbrl_files = self.__get_xbrl_files(xbrl_schema_path)

        # XBRLファイルのリストをループします。
        for xbrl_file in xbrl_files:
            # ファイル名を取得します。
            xbrl_file_name = xbrl_file.split('/')[-1:][0]
            # ファイルのディレクトリを取得します。
            xbrl_file_dir = '/'.join(xbrl_file.split('/')[3:-1])
            # ファイルのパスを取得します。
            xbrl_file_path = f'{ self.__Xbrl_save_dir }/{xbrl_file_dir}/{ xbrl_file_name }'
            # ファイルパスをリストに追加します。
            lists.append(xbrl_file_path)
            # ファイルがローカルに存在するか確認します。
            if os.path.exists(xbrl_file_path):
                continue
            # xbrl_file_pathのディレクトリが存在しない場合、ディレクトリを作成します。
            if not os.path.exists(os.path.dirname(f'{ self.__Xbrl_save_dir }/{ xbrl_file_dir }/')):
                os.makedirs(os.path.dirname(f'{ self.__Xbrl_save_dir }/{ xbrl_file_dir }/'))
            # ファイルをダウンロードします。
            response = requests.get(xbrl_file)
            # ファイルを保存します。
            with open(xbrl_file_path, 'wb') as f:
                f.write(response.content)
            # 待機時間を設定します。
            time.sleep(sleep_time)

        return lists

    def load_xbrl_files_from_list(self, url_list:list[str], sleep_time = 2):
        """ XBRLファイルをリストからダウンロードします。
            保存したXBRLファイルのローカルパスのリストを返します。

        Args:
            url_list (list): XBRLファイルのURLリスト

        Yields:
            xbrl_file (str): XBRLファイルのURL
            xbrl_file_path (str): XBRLファイルのローカルパス

        Examples:
            >>> xbrl_download_manager = XBRLDownloadManager(xbrl_schema_path, Xbrl_save_dir)
            >>> for xbrl_file_path in xbrl_download_manager.download_xbrl_files():
            >>>     print(xbrl_file_path)
            output:
            [
            '/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab.xml',
            '/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab-en.xml',
            ]
        """
        if sleep_time < 2:
            raise ValueError('待機時間は2秒以上に設定してください。')

        # XBRLファイルのリストをループします。
        for xbrl_file in url_list:
            # httpが含まれていない場合、スキップします。
            if "http" not in xbrl_file:
                continue
            # ファイル名を取得します。
            xbrl_file_name = xbrl_file.split('/')[-1:][0]
            # ファイルのディレクトリを取得します。
            xbrl_file_dir = '/'.join(xbrl_file.split('/')[3:-1])
            # ファイルのパスを取得します。
            xbrl_file_path = f'{ self.__Xbrl_save_dir }/{xbrl_file_dir}/{ xbrl_file_name }'
            # ファイルがローカルに存在するか確認します。
            if os.path.exists(xbrl_file_path):
                yield xbrl_file, xbrl_file_path
                continue
            # xbrl_file_pathのディレクトリが存在しない場合、ディレクトリを作成します。
            if not os.path.exists(os.path.dirname(f'{ self.__Xbrl_save_dir }/{ xbrl_file_dir }/')):
                os.makedirs(os.path.dirname(f'{ self.__Xbrl_save_dir }/{ xbrl_file_dir }/'))
            # ファイルをダウンロードします。
            response = requests.get(xbrl_file)
            # ファイルを保存します。
            with open(xbrl_file_path, 'wb') as f:
                f.write(response.content)
            # 待機時間を設定します。
            time.sleep(sleep_time)

            yield xbrl_file, xbrl_file_path
