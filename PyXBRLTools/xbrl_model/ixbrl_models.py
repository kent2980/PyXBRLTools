from abc import ABC, abstractmethod
from PyXBRLTools.xbrl_manager.ixbrl_manager import IxbrlManager
from PyXBRLTools.xbrl_manager.xbrl_label_manager import XbrlLabelManager
from PyXBRLTools.xbrl_manager.xbrl_link_manager import XbrlLinkManager, XbrlLinkType
import re

class BaseIxbrlModel(ABC):
    """ iXBRLモデルの基底クラス """

    def __init__(self, xbrl_directory_path: str, load_label_directory: str):
        """ コンストラクタ """
        # マネージャークラスを初期化
        self.__ixbrl_manager = IxbrlManager(xbrl_directory_path)  # iXBRLマネージャーを初期化
        self.__label_manager = XbrlLabelManager(xbrl_directory_path, load_label_directory)  # ラベルマネージャーを初期化
        self.__link_manager = XbrlLinkManager(xbrl_directory_path)  # リンクマネージャーを初期化

    @abstractmethod
    def __str__(self):
        """ユーザー向けにオブジェクトの文字列表現を返します。"""
        pass

    @abstractmethod
    def __repr__(self):
        """ 開発者向けにオブジェクトの文字列表現を返します。"""
        pass

class IxNonFraction(BaseIxbrlModel):

    def __init__(self, xbrl_directory_path: str, load_label_directory: str):
        super().__init__()  # ベースクラスのコンストラクタを呼び出す
        self.__ixbrl_manager: IxbrlManager = self._BaseIxbrlModel__ixbrl_manager  # ベースクラスからixbrl_managerインスタンスにアクセスする
        self.__label_manager: XbrlLabelManager = self._BaseIxbrlModel__label_manager  # ベースクラスからlabel_managerインスタンスにアクセスする
        self.__link_manager: XbrlLinkManager = self._BaseIxbrlModel__link_manager  # ベースクラスからlink_managerインスタンスにアクセスする

        # プロパティを初期化する
        self.__ixbrl_numeric = None
        self.__label_locs = None
        self.__label_arcs = None
        self.__labels = None
        self.__cal_link_locs = None
        self.__cal_link_arcs = None
        self.__def_link_locs = None
        self.__def_link_arcs = None
        self.__pre_link_locs = None
        self.__pre_link_arcs = None

        self.__links = {}

    @property
    def ixbrl_numeric(self):
        """ixbrl_numericプロパティ"""
        if self.__ixbrl_numeric is None:
            self.__ixbrl_numeric = self.__ixbrl_manager.ix_non_fractions
            self.links['label_names'] = list(set(self.__ixbrl_numeric['name'].to_list()))
        return self.__ixbrl_numeric

    @property
    def label_locs(self):
        """label_locsプロパティ"""
        if self.__links['label_names'] is None:
            raise ValueError('label_namesプロパティがNoneです。')
        if self.__label_locs is None:
            self.__label_locs = self.__label_manager.get_label_locs(self.__links['label_names'])
        return self.__label_locs

    @property
    def label_arcs(self, xlink_label: list[str]):
        """label_arcsプロパティ"""
        if self.__label_arcs is None:
            self.__label_arcs = self.__label_manager.get_label_arcs(xlink_label)
        return self.__label_arcs

    @property
    def labels(self, xlink_to: list[str]):
        """labelsプロパティ"""
        if self.__labels is None:
            self.__labels = self.__label_manager.get_labels(xlink_to)
        return self.__labels

    @property
    def cal_link_locs(self, label_names: list[str] = None):
        """cal_link_locsプロパティ"""
        if self.__cal_link_locs is None:
            self.__link_manager.link_type = XbrlLinkType.CAL
            self.__cal_link_locs = self.__link_manager.get_link_locs(label_names)
        return self.__cal_link_locs

    @property
    def cal_link_arcs(self, xlink_href: list[str] = None):
        """cal_link_arcsプロパティ"""
        if self.__cal_link_arcs is None:
            self.__link_manager.link_type = XbrlLinkType.CAL
            self.__cal_link_arcs = self.__link_manager.get_link_arcs(xlink_href)
        return self.__cal_link_arcs

    @property
    def def_link_locs(self, label_names: list[str] = None):
        """def_link_locsプロパティ"""
        if self.__def_link_locs is None:
            self.__link_manager.link_type = XbrlLinkType.DEF
            self.__def_link_locs = self.__link_manager.get_link_locs(label_names)
        return self.__def_link_locs

    @property
    def def_link_arcs(self, xlink_href: list[str] = None):
        """def_link_arcsプロパティ"""
        if self.__def_link_arcs is None:
            self.__link_manager.link_type = XbrlLinkType.DEF
            self.__def_link_arcs = self.__link_manager.get_link_arcs(xlink_href)
        return self.__def_link_arcs

    @property
    def pre_link_locs(self, label_names: list[str] = None):
        """pre_link_locsプロパティ"""
        if self.__pre_link_locs is None:
            self.__link_manager.link_type = XbrlLinkType.PRE
            self.__pre_link_locs = self.__link_manager.get_link_locs(label_names)
        return self.__pre_link_locs

    @property
    def pre_link_arcs(self, xlink_href: list[str] = None):
        """pre_link_arcsプロパティ"""
        if self.__pre_link_arcs is None:
            self.__link_manager.link_type = XbrlLinkType.PRE
            self.__pre_link_arcs = self.__link_manager.get_link_arcs(xlink_href)
        return self.__pre_link_arcs
