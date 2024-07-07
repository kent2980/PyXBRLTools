from app.manager import (
    CalLinkManager,
    DefLinkManager,
    IxbrlManager,
    LabelManager,
    PreLinkManager,
)
from app.models import BaseXbrlModel


class EdifModel(BaseXbrlModel):
    """決算短信(国際会計基準)のXBRLファイルを扱うクラス"""

    def __init__(self, xbrl_zip_path, output_path) -> None:
        super().__init__(xbrl_zip_path, output_path)
        self._xbrl_type_check("edif", ("ixbrl.htm", "lab", "pre", "cal", "def"))
        self._initialize_managers()

    def _initialize_managers(self):
        """managerクラスを初期化"""
        directory_path = self.directory_path
        self.ixbrl_manager = IxbrlManager(directory_path).set_xbrl_id(self.xbrl_id)
        self.label_manager = self._create_manager(LabelManager, "label")
        self.cal_manager = self._create_manager(CalLinkManager, "cal").set_xbrl_id(
            self.xbrl_id
        )
        self.pre_manager = self._create_manager(PreLinkManager, "pre").set_xbrl_id(
            self.xbrl_id
        )
        self.def_manager = self._create_manager(DefLinkManager, "def").set_xbrl_id(
            self.xbrl_id
        )
        # self.qualitative_manager = self._create_manager(QualitativeManager, "qualitative")

    def get_ixbrl(self):
        """iXBRLデータを取得するメソッド"""
        value = self._get_data_frames(
            self.ixbrl_manager,
            "set_ix_non_fraction",
            "set_ix_non_numeric",
            "set_ix_header",
        )
        return self._get_xbrl_id(value)

    def get_label(self):
        """ラベルリンクベースのデータを取得するメソッド"""
        return self._get_data_frames(
            self.label_manager,
            "set_link_label_locs",
            "set_link_label_arcs",
            "set_link_labels",
        )

    def get_cal_linkbase(self):
        """カレンダーリンクベースのデータを取得するメソッド"""
        value = self._get_data_frames(
            self.cal_manager, "set_link_locs", "set_link_arcs"
        )
        return self._get_xbrl_id(value)

    def get_pre_linkbase(self):
        """プレゼンテーションリンクベースのデータを取得するメソッド"""
        value = self._get_data_frames(
            self.pre_manager, "set_link_locs", "set_link_arcs"
        )
        return self._get_xbrl_id(value)

    def get_def_linkbase(self):
        """定義リンクベースのデータを取得するメソッド"""
        value = self._get_data_frames(
            self.def_manager, "set_link_locs", "set_link_arcs"
        )
        return self._get_xbrl_id(value)

    def get_all_data(self):
        """全てのデータを取得するメソッド"""
        dict = {
            "ixbrl": self.get_ixbrl(),
            "label": self.get_label(),
            "cal": self.get_cal_linkbase(),
            "pre": self.get_pre_linkbase(),
            "def": self.get_def_linkbase(),
        }
        return dict
