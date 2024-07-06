from app.manager import DefLinkManager, IxbrlManager, LabelManager
from app.models import BaseXbrlModel


class RvfcModel(BaseXbrlModel):
    """
    業績予想修正に関するお知らせのXBRLファイルを扱うクラス

    Args:
        xbrl_zip_path (str): パースするXBRLファイルのZIPパス
        output_path (str): 出力先のパス

    Attributes:
        ixbrl_manager (IxbrlManager): iXBRLデータを管理するマネージャークラス
        label_manager (LabelManager): ラベルデータを管理するマネージャークラス
        def_manager (DefLinkManager): 定義リンクベースデータを管理するマネージャークラス

    Methods:
        get_ixbrl: iXBRLデータを取得するメソッド
        get_label: ラベルデータを取得するメソッド
        get_def_linkbase: 定義リンクベースデータを取得するメソッド

    Examples:
        >>> xbrl_zip_path = "path/to/xbrl_zip"
        >>> output_path = "path/to/output"
        >>> rvfc_model = RvfcModel(xbrl_zip_path, output_path)
        >>> ix_non_fraction, ix_non_numeric = rvfc_model.get_ixbrl()
        >>> locs, arcs, labels = rvfc_model.get_label()
        >>> locs, arcs = rvfc_model.get_def_linkbase()
    """

    def __init__(self, xbrl_zip_path, output_path) -> None:
        super().__init__(xbrl_zip_path, output_path)
        self._xbrl_type_check("rvfc", ("ixbrl.htm", "def", "xsd"))
        self._initialize_managers()

    def _initialize_managers(self):
        """managerクラスを初期化"""
        directory_path = self.directory_path
        self.ixbrl_manager = IxbrlManager(directory_path).set_xbrl_id(self.xbrl_id)
        self.label_manager = self._create_manager(LabelManager, "label")
        self.def_manager = self._create_manager(DefLinkManager, "def").set_xbrl_id(
            self.xbrl_id
        )

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
            "def": self.get_def_linkbase(),
        }
        return dict
