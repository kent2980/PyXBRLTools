import zipfile

from PyXBRLTools.xbrl_model.edif_model import EdifModel
from PyXBRLTools.xbrl_model.edit_model import EditModel
from PyXBRLTools.xbrl_model.edjp_model import EdjpModel
from PyXBRLTools.xbrl_model.edus_model import EdusModel
from PyXBRLTools.xbrl_model.efjp_model import EfjpModel
from PyXBRLTools.xbrl_model.rejp_model import RejpModel
from PyXBRLTools.xbrl_model.rrdf_model import RrdfModel
from PyXBRLTools.xbrl_model.rrfc_model import RrfcModel
from PyXBRLTools.xbrl_model.rvdf_model import RvdfModel
from PyXBRLTools.xbrl_model.rvfc_model import RvfcModel


class XbrlReader:
    def __init__(self, xbrl_zip_path, output_path) -> None:
        self.xbrl_zip_path = xbrl_zip_path
        self.output_path = output_path
        self.xbrl_type = self.__get_xbrl_type()
        self.model = self.get_model()

    def __get_xbrl_type(self):
        """XBRLファイルの種類を取得するメソッド"""
        with zipfile.ZipFile(self.xbrl_zip_path, "r") as z:
            file_list = z.infolist()
        # file_listからixbrl.htmを再起的に取得
        ixbrl_files = [file for file in file_list if "ixbrl.htm" in file.filename]
        if len(ixbrl_files) == 1:
            return ixbrl_files[0].filename.split("-")[1]
        elif len(ixbrl_files) > 1:
            for ixbrl_file in ixbrl_files:
                if "sm" in ixbrl_file.filename:
                    return ixbrl_file.filename.split("-")[1][2:6]

    def get_model(self):
        if self.xbrl_type == "edif":
            return EdifModel(self.xbrl_zip_path, self.output_path)
        elif self.xbrl_type == "edit":
            return EditModel(self.xbrl_zip_path, self.output_path)
        elif self.xbrl_type == "edjp":
            return EdjpModel(self.xbrl_zip_path, self.output_path)
        elif self.xbrl_type == "edus":
            return EdusModel(self.xbrl_zip_path, self.output_path)
        elif self.xbrl_type == "efjp":
            return EfjpModel(self.xbrl_zip_path, self.output_path)
        elif self.xbrl_type == "rejp":
            return RejpModel(self.xbrl_zip_path, self.output_path)
        elif self.xbrl_type == "rrdf":
            return RrdfModel(self.xbrl_zip_path, self.output_path)
        elif self.xbrl_type == "rrfc":
            return RrfcModel(self.xbrl_zip_path, self.output_path)
        elif self.xbrl_type == "rvdf":
            return RvdfModel(self.xbrl_zip_path, self.output_path)
        elif self.xbrl_type == "rvfc":
            return RvfcModel(self.xbrl_zip_path, self.output_path)
