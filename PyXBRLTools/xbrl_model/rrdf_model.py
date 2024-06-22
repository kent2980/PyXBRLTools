from PyXBRLTools.xbrl_model.base_xbrl_model import BaseXbrlModel
from PyXBRLTools.xbrl_manager.ixbrl_manager import IxbrlManager
from PyXBRLTools.xbrl_manager.label_manager import LabelManager
from PyXBRLTools.xbrl_manager.link_manager import DefLinkManager

class RrdfModel(BaseXbrlModel):
    """ 分配予想の修正に関するお知らせのXBRLファイルを扱うクラス """
    def __init__(self, xbrl_zip_path, output_path) -> None:
        super().__init__(xbrl_zip_path, output_path)
        self._xbrl_type_check("rrdf", ("ixbrl.htm", "def"))
        self._initialize_managers()

    def _initialize_managers(self):
        """ managerクラスを初期化 """
        directory_path = self.directory_path
        self.ixbrl_manager = IxbrlManager(directory_path).set_xbrl_id(self.xbrl_id)
        self.label_manager = self._create_manager(LabelManager, "label")
        self.def_manager = self._create_manager(DefLinkManager, "def").set_xbrl_id(self.xbrl_id)

    def get_ixbrl(self):
        """iXBRLデータを取得するメソッド"""
        return self._get_data_frames(self.ixbrl_manager, "set_ix_non_fraction", "set_ix_non_numeric", "set_ix_header")

    def get_label(self):
        """ラベルリンクベースのデータを取得するメソッド"""
        return self._get_data_frames(self.label_manager, "set_link_locs", "set_link_label_arcs", "set_link_labels")

    def get_def_linkbase(self):
        """定義リンクベースのデータを取得するメソッド"""
        return self._get_data_frames(self.def_manager, "set_link_locs", "set_link_arcs")
