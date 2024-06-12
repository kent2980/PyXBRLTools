from abc import ABC, abstractmethod
import time
from xbrl_manager.ixbrl_manager import IxbrlManager
from xbrl_manager.xbrl_label_manager import XbrlLabelManager
from xbrl_manager.xbrl_link_manager import XbrlLinkManager, XbrlLinkType
from pandas import DataFrame
import asyncio

class BaseIxbrlModel(ABC):
    """ iXBRLモデルの基底クラス """

    def __init__(self, xbrl_directory_path: str, load_label_directory: str):
        """ コンストラクタ """
        # マネージャークラスを初期化
        self.__ixbrl_manager = IxbrlManager(xbrl_directory_path)  # iXBRLマネージャーを初期化
        self.__label_manager = XbrlLabelManager(xbrl_directory_path, load_label_directory)  # ラベルマネージャーを初期化
        self.__link_manager = XbrlLinkManager(xbrl_directory_path)  # リンクマネージャーを初期化

class IxbrlModel(BaseIxbrlModel):
    """ iXBRL数値情報モデルクラス

    Attributes:
        ixbrl_numeric (DataFrame): XBRL数値情報
        label_locs (DataFrame): ラベル情報
        label_arcs (DataFrame): ラベルアーク情報
        labels (DataFrame): ラベル情報
        cal_link_locs (DataFrame): 計算リンク情報
        cal_link_arcs (DataFrame): 計算リンクアーク情報
        def_link_locs (DataFrame): 定義リンク情報
        def_link_arcs (DataFrame): 定義リンクアーク情報
        pre_link_locs (DataFrame): 表示リンク情報
        pre_link_arcs (DataFrame): 表示リンクアーク情報

    Args:
        xbrl_directory_path (str): XBRLディレクトリのパス
        load_label_directory (str): ラベルディレクトリのパス

    Raises:
        ValueError: プロパティの設定に失敗した場合に発生します。

    Examples:
        >>> from PyXBRLTools.xbrl_model.ixbrl_models import IxNonFraction
        >>> ix_non_fraction = IxNonFraction('XBRLディレクトリのパス', 'ラベルディレクトリのパス')
        >>> print(ix_non_fraction.ixbrl_numeric)
        >>> print(ix_non_fraction.label_locs)
        >>> print(ix_non_fraction.label_arcs)
        >>> print(ix_non_fraction.labels)
        >>> print(ix_non_fraction.cal_link_locs)
        >>> print(ix_non_fraction.cal_link_arcs)
        >>> print(ix_non_fraction.def_link_locs)
        >>> print(ix_non_fraction.def_link_arcs)
        >>> print(ix_non_fraction.pre_link_locs)
        >>> print(ix_non_fraction.pre_link_arcs)
    """

    def __init__(self, xbrl_directory_path: str, load_label_directory: str):
        super().__init__(xbrl_directory_path, load_label_directory)  # ベースクラスのコンストラクタを呼び出す
        self.__ixbrl_manager: IxbrlManager = self._BaseIxbrlModel__ixbrl_manager  # ベースクラスからixbrl_managerインスタンスにアクセスする
        self.__label_manager: XbrlLabelManager = self._BaseIxbrlModel__label_manager  # ベースクラスからlabel_managerインスタンスにアクセスする
        self.__link_manager: XbrlLinkManager = self._BaseIxbrlModel__link_manager  # ベースクラスからlink_managerインスタンスにアクセスする

        asyncio.run(self.async_inicialize())

    async def async_inicialize(self):

        # 処理時間を計測する
        start = time.time()

        # プロパティを初期化する
        self.__ix_non_fraction = None
        self.__ix_non_numeric = None

        # プロパティを設定する
        await self.__set_ix_non_fraction()
        await self.__set_ix_non_numeric()

        # 処理時間を出力する
        elapsed_time = time.time() - start
        print(f'処理時間: {elapsed_time} [sec]')

    async def __set_ix_non_fraction(self):
        """ プロパティを設定します。

        Raises:
            ValueError: プロパティの設定に失敗した場合に発生します。
        """
        # XBRL数値情報を取得
        ix_non_fraction = self.__ixbrl_manager.ix_non_fractions

        # ラベル情報を取得
        label_locs = self.__label_manager.label_locs
        label_arcs = self.__label_manager.label_arcs
        labels = self.__label_manager.labels

        # 計算リンク情報を取得
        self.__link_manager.link_type = XbrlLinkType.CAL
        cal_link_locs = self.__link_manager.link_locs
        cal_link_arcs = self.__link_manager.link_arcs

        # 定義リンク情報を取得
        self.__link_manager.link_type = XbrlLinkType.DEF
        def_link_locs = self.__link_manager.link_locs
        def_link_arcs = self.__link_manager.link_arcs

        # 表示リンク情報を取得
        self.__link_manager.link_type = XbrlLinkType.PRE
        pre_link_locs = self.__link_manager.link_locs
        pre_link_arcs = self.__link_manager.link_arcs

        # ラベルを抽出
        label_locs = label_locs[label_locs['xlink_href'].isin(ix_non_fraction['name'])]
        label_arcs = label_arcs[label_arcs['xlink_from'].isin(label_locs['xlink_label'])]
        labels = labels[labels['xlink_label'].isin(label_arcs['xlink_to'])]

        cal_link_locs = cal_link_locs[cal_link_locs['xlink_href'].isin(ix_non_fraction['name'])]
        cal_link_arcs = cal_link_arcs[cal_link_arcs['xlink_to'].isin(cal_link_locs['xlink_label'])]

        def_link_locs = def_link_locs[def_link_locs['xlink_href'].isin(ix_non_fraction['name'])]
        def_link_arcs = def_link_arcs[def_link_arcs['xlink_to'].isin(def_link_locs['xlink_label'])]

        pre_link_locs = pre_link_locs[pre_link_locs['xlink_href'].isin(ix_non_fraction['name'])]
        pre_link_arcs = pre_link_arcs[pre_link_arcs['xlink_to'].isin(pre_link_locs['xlink_label'])]
        # プロパティを設定する
        self.__ix_non_fraction = {
            'ix_non_fraction': ix_non_fraction,
            'inf_label_locs': label_locs,
            'inf_label_arcs': label_arcs,
            'inf_labels': labels,
            'cal_link_locs': cal_link_locs,
            'cal_link_arcs': cal_link_arcs,
            'def_link_locs': def_link_locs,
            'def_link_arcs': def_link_arcs,
            'pre_link_locs': pre_link_locs,
            'pre_link_arcs': pre_link_arcs
        }

    async def __set_ix_non_numeric(self):
        """ プロパティを設定します。

        Raises:
            ValueError: プロパティの設定に失敗した場合に発生します。
        """
        # XBRL数値情報を取得
        ix_non_numeric = self.__ixbrl_manager.ix_non_numerics

        # ラベル情報を取得
        label_locs = self.__label_manager.label_locs
        label_arcs = self.__label_manager.label_arcs
        labels = self.__label_manager.labels

        # ラベル情報を抽出
        label_locs = label_locs[label_locs['xlink_href'].isin(ix_non_numeric['name'])]
        label_arcs = label_arcs[label_arcs['xlink_from'].isin(label_locs['xlink_label'])]
        labels = labels[labels['xlink_label'].isin(label_arcs['xlink_to'])]

        # プロパティを設定する
        self.__ix_non_numeric = {
            'ix_non_numeric': ix_non_numeric,
            'inn_label_locs': label_locs,
            'inn_label_arcs': label_arcs,
            'inn_labels': labels
        }

    @property
    def ix_non_fraction(self) -> dict:
        """ XBRL数値情報を取得します。

        Returns:
            dict: XBRL数値情報

        Raises:
            ValueError: XBRL数値情報の取得に失敗した場合に発生します。
        """
        return self.__ix_non_fraction

    @property
    def ix_non_numeric(self) -> dict:
        """ XBRL数値情報を取得します。

        Returns:
            dict: XBRL数値情報

        Raises:
            ValueError: XBRL数値情報の取得に失敗した場合に発生します。
        """
        return self.__ix_non_numeric