from abc import ABC, abstractmethod
from xbrl_parser.xml_label_parser import XmlLabelParser
from xbrl_manager.xbrl_path_manager import XbrlPathManager
import os
from xbrl_manager.xbrl_download_manager import XBRLDownloadManager
from pandas import DataFrame
import pandas as pd

class LabelLanguege:
    """ XBRLラベルの言語を表すクラスです。 """
    JA = 'ja'
    EN = 'en'

class BaseXbrlLabelManager(ABC):
    """
    XBRLラベルマネージャーの基底クラスです。

    Attributes:
        __xbrl_directory_path (str): XBRLファイルが格納されているディレクトリのパス
        __xbrl_path_manager (XbrlPathManager): XBRLパスマネージャーのインスタンス
        __label_paths (dict): ラベルファイルのパス
        __label_parser (XmlLabelParser): XMLラベルパーサのインスタンス

    Properties:
        xbrl_directory_path (str): XBRLディレクトリのパスを取得するプロパティ

    Methods:
        __init__: コンストラクタ
    """

    def __init__(self, xbrl_directory_path: str, load_label_directory:str, lang:str = LabelLanguege.JA):
        """
        コンストラクタ

        Parameters:
            xbrl_directory_path (str): XBRLファイルが格納されているディレクトリのパス
        """
        # langがLabelLanguageクラスの定数でない場合、エラーを出力
        if lang not in [LabelLanguege.JA, LabelLanguege.EN]:
            raise ValueError(f"langは{LabelLanguege.JA}または{LabelLanguege.EN}を指定してください。")

        # 言語設定をインスタンス変数に格納
        self.__language = lang

        # XBRLディレクトリのパスをインスタンス変数に格納
        self.__xbrl_directory_path = xbrl_directory_path

        self.__load_label_directory = load_label_directory

        # XbrlPathManagerクラスのインスタンスを作成し、XBRLディレクトリのパスを渡す
        self.__xbrl_path_manager = XbrlPathManager(xbrl_directory_path)

        # XbrlPathManagerから取得したラベルファイルのパスをインスタンス変数に格納
        self.__label_paths = self.__xbrl_path_manager.lab_path

        # langがjaの場合、ラベルファイルのパスをlab.xmlで終わるものを抽出
        if lang == LabelLanguege.JA:
            self.__label_paths = [label_path for label_path in self.__label_paths if label_path['file_path'].endswith('lab.xml')]
        # langがenの場合、ラベルファイルのパスをlab-en.xmlで終わるものを抽出
        elif lang == LabelLanguege.EN:
            self.__label_paths = [label_path for label_path in self.__label_paths if label_path['file_path'].endswith('lab-en.xml')]
        else:
            raise ValueError(f"langは{LabelLanguege.JA}または{LabelLanguege.EN}を指定してください。")

        # ラベルファイルをローカルフォルダに読み込む
        self.__label_paths = self._load_label_files(load_label_directory)

        # XmlLabelParserクラスのインスタンスを作成
        self.__label_parser = XmlLabelParser()

        self.__inicialize_properties()

    def __inicialize_properties(self):
        """
        プロパティを初期化するメソッドです。
        """
        self.__label_arcs = None
        self.__label_locs = None
        self.__role_refs = None
        self.__labels = None

    @property
    def xbrl_directory_path(self):
        """
        XBRLディレクトリのパスを取得するプロパティです。
        """
        return self.__xbrl_directory_path

    @xbrl_directory_path.setter
    def xbrl_directory_path(self, value):
        """
        XBRLディレクトリのパスを設定するプロパティです。

        Parameters:
            value (str): 設定するXBRLディレクトリのパス
        """

        # XBRLディレクトリのパスを設定
        self.__xbrl_directory_path = value

        # XBRLパスマネージャーのXBRLディレクトリのパスも設定
        self.__xbrl_path_manager.xbrl_directory_path = value

        # ラベルパスをXBRLパスマネージャーから取得
        self.__label_paths = self.__xbrl_path_manager.label_path

        # プロパティを初期化
        self.__inicialize_properties

    @property
    def load_label_directory(self):
        """
        ラベルファイルをロードするディレクトリのパスを取得するプロパティです。
        """
        return self.__load_label_directory

    @load_label_directory.setter
    def load_label_directory(self, value):
        """
        ラベルファイルをロードするディレクトリのパスを設定するプロパティです。

        Parameters:
            value (str): 設定するラベルファイルをロードするディレクトリのパス
        """
        self.__load_label_directory = value

    @property
    def label_paths(self):
        """
        ラベルファイルのパスを取得するプロパティです。
        """
        return self.__label_paths

    @property
    def language(self):
        """
        言語設定を取得するプロパティです。
        """
        return self.__language

    @language.setter
    def language(self, value):
        """
        言語設定を設定するプロパティです。

        Parameters:
            value (str): 設定する言語設定
        """
        # langがLabelLanguageクラスの定数でない場合、エラーを出力
        if value not in [LabelLanguege.JA, LabelLanguege.EN]:
            raise ValueError(f"langは{LabelLanguege.JA}または{LabelLanguege.EN}を指定してください。")

        # 言語設定をインスタンス変数に格納
        self.__language = value

    # ラベルをローカルフォルダに読み込むメソッド
    @abstractmethod
    def _load_label_files(self, load_label_directory:str):
        """
        ラベルをローカルフォルダに読み込むメソッドです。
        """
        pass

    @property
    @abstractmethod
    def label_arcs(self):
        """
        ラベルアークを取得するメソッドです。
        """
        pass

    @property
    @abstractmethod
    def label_locs(self):
        """
        ラベルロケーションを取得するメソッドです。
        """
        pass

    @property
    @abstractmethod
    def role_refs(self):
        """
        ロール参照を取得するメソッドです。
        """
        pass

    @property
    @abstractmethod
    def labels(self):
        """
        ラベルを取得するメソッドです。
        """
        pass

class XbrlLabelManager(BaseXbrlLabelManager):
    """ ラベルマネージャ

    Properties:
        label_paths (dict): ラベルファイルのパスを取得するプロパティ
        language (str): 言語設定を取得するプロパティ

    Methods:
        __init__: コンストラクタ
        get_label_arcs: ラベルアークを取得するメソッド
        get_label_locs: ラベルロケーションを取得するメソッド
        get_role_refs: ロール参照を取得するメソッド
        get_labels: ラベルを取得するメソッド
        _load_label_files: ラベルをローカルフォルダに読み込むメソッド
    """
    def _load_label_files(self, load_label_directory:str) -> dict[str, str]:
        """
        ラベルをローカルフォルダに読み込むメソッドです。

        Args:
            load_label_directory (str): ラベルファイルをロードするディレクトリのパス

        Returns:
            label_paths (dict): ラベルファイルのパス

        Raises:
            FileNotFoundError: ディレクトリが存在しない場合

        Examples:
            >>> label_paths = self._load_label_files(load_label_directory)
            >>> print(label_paths)
            output:
            [
                {
                    'document_type': 'jpcrp',
                    'file_path': 'local/jpcrp_2023-12-01_lab.xml',
                    'path_type': 'local'
                },
                {
                    'file_path': 'local/jpcrp_2023-12-01_lab-en.xml',
                    'path_type': 'local'
                }
            ]
        """
        # ディレクトリが有効かどうかを確認
        if not os.path.isdir(load_label_directory):
            raise FileNotFoundError(f"ディレクトリが存在しません。: {load_label_directory}")

        # XBRLダウンロードマネージャーのインスタンスを作成
        download_manager = XBRLDownloadManager(load_label_directory)

        # ラベルファイルのパスを取得
        label_paths = DataFrame(self._BaseXbrlLabelManager__label_paths)

        # ラベルファイルのパスをリストに変換
        label_paths_list = label_paths['file_path'].tolist()

        # ラベルファイルをローカルフォルダにダウンロード
        for file_path, local_path in download_manager.load_xbrl_files_from_list(label_paths_list):
            # labelpathsのfile_pathをlocal_pathに変更
            label_paths['file_path'] = label_paths['file_path'].replace(file_path, local_path)

        # lbel_pathsのpath_typeを全てlocalに変更
        label_paths['path_type'] = 'local'

        # label_pathsを辞書型に変換
        label_paths = label_paths.to_dict(orient='records')

        # ローカルファイルのパスを返す
        return label_paths

    @property
    def label_arcs(self) -> DataFrame:

        """
        ラベルアークを取得するメソッドです。

        Returns:
            label_arcs (DataFrame): ラベルアーク

        Examples:
            >>> label_arcs = self.get_label_arcs()
            >>> print(label_arcs)
            output:
            [
                {
                    'arcrole': 'http://www.xbrl.org/2003/arcrole/concept-label',
                    'from': 'jpcrp_cor_2021-03-31_lab_en',
                    'to': 'jpcrp_cor_2021-03-31_lab_en'
                },
                {
                    'arcrole': 'http://www.xbrl.org/2003/arcrole/concept-label',
                    'from': 'jpcrp_cor_2021-03-31_lab_en',
                    'to': 'jpcrp_cor_2021-03-31_lab_en'
                }
            ]
        """
        if self._BaseXbrlLabelManager__label_arcs is not None:
            return self._BaseXbrlLabelManager__label_arcs

        parser:XmlLabelParser = self._BaseXbrlLabelManager__label_parser

        label_arcs = None
        for label_path in self._BaseXbrlLabelManager__label_paths:
            parser.file_path = label_path['file_path']
            if label_arcs is None:
                label_arcs = parser.link_label_arcs
            else:
                label_arcs = pd.concat([label_arcs, parser.link_label_arcs])

        self._BaseXbrlLabelManager__label_arcs = label_arcs.drop_duplicates()

        return self._BaseXbrlLabelManager__label_arcs

    @property
    def label_locs(self) -> DataFrame:
        """
        ラベルロケーションを取得するメソッドです。

        Returns:
            label_locs (DataFrame): ラベルロケーション

        Examples:
            >>> label_locs = self.get_label_locs()
            >>> print(label_locs)
            output:
            [
                {
                    'label': 'jpcrp_cor_2021-03-31_lab_en',
                    'loc': 'jpcrp_cor_2021-03-31_lab_en'
                },
                {
                    'label': 'jpcrp_cor_2021-03-31_lab_en',
                    'loc': 'jpcrp_cor_2021-03-31_lab_en'
                }
            ]
        """
        if self._BaseXbrlLabelManager__label_locs is not None:
            return self._BaseXbrlLabelManager__label_locs

        parser:XmlLabelParser = self._BaseXbrlLabelManager__label_parser

        label_locs = None
        for label_path in self._BaseXbrlLabelManager__label_paths:
            parser.file_path = label_path['file_path']
            if label_locs is None:
                label_locs = parser.link_locs
            else:
                label_locs = pd.concat([label_locs, parser.link_locs])

        self._BaseXbrlLabelManager__label_locs = label_locs.drop_duplicates()

        return self._BaseXbrlLabelManager__label_locs

    @property
    def role_refs(self) -> DataFrame:
        """
        ロール参照を取得するメソッドです。

        Returns:
            role_refs (DataFrame): ロール参照

        Examples:
            >>> role_refs = self.get_role_refs()
            >>> print(role_refs)
            output:
            [
                {
                    'role': 'jpcrp_cor_2021-03-31_lab_en',
                    'ref': 'jpcrp_cor_2021-03-31_lab_en'
                },
                {
                    'role': 'jpcrp_cor_2021-03-31_lab_en',
                    'ref': 'jpcrp_cor_2021-03-31_lab_en'
                }
            ]
        """
        if self._BaseXbrlLabelManager__role_refs is not None:
            return self._BaseXbrlLabelManager__role_refs

        parser:XmlLabelParser = self._BaseXbrlLabelManager__label_parser

        role_refs = None
        for label_path in self._BaseXbrlLabelManager__label_paths:
            parser.file_path = label_path['file_path']
            if role_refs is None:
                role_refs = parser.role_refs
            else:
                role_refs = pd.concat([role_refs, parser.role_refs])

        self._BaseXbrlLabelManager__role_refs = role_refs.drop_duplicates()

        return self._BaseXbrlLabelManager__role_refs

    @property
    def labels(self) -> DataFrame:
        """
        ラベルを取得するメソッドです。

        Returns:
            labels (DataFrame): ラベル

        Examples:
            >>> labels = self.get_labels()
            >>> print(labels)
            output:
            [
                {
                    'label': 'jpcrp_cor_2021-03-31_lab_en',
                    'label_text': 'jpcrp_cor_2021-03-31_lab_en'
                },
                {
                    'label': 'jpcrp_cor_2021-03-31_lab_en',
                    'label_text': 'jpcrp_cor_2021-03-31_lab_en'
                }
            ]
        """
        if self._BaseXbrlLabelManager__labels is not None:
            return self._BaseXbrlLabelManager__labels

        parser:XmlLabelParser = self._BaseXbrlLabelManager__label_parser

        labels = None
        for label_path in self._BaseXbrlLabelManager__label_paths:
            parser.file_path = label_path['file_path']
            if labels is None:
                labels = parser.link_labels
            else:
                labels = pd.concat([labels, parser.link_labels])

        self._BaseXbrlLabelManager__labels = labels.drop_duplicates()

        return self._BaseXbrlLabelManager__labels