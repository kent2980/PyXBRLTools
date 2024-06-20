from pathlib import Path
import shutil
import zipfile
from PyXBRLTools.xbrl_exception.xbrl_model_exception import NotXbrlDirectoryException

class BaseXbrlModel:
    def __init__(self, xbrl_zip_path) -> None:
        # XBRLファイルのzipファイルのパスを指定
        self.__xbrl_zip_path = Path(xbrl_zip_path)
        # XBRLファイルを解凍したディレクトリのパスを取得
        self.__directory_path = self.__unzip_xbrl()
        self.__xbrl_type = self.__xbrl_type()

    def __del__(self):
        directory_path = Path(self.directory_path)
        if directory_path.exists() and directory_path.is_dir():
            shutil.rmtree(directory_path.as_posix())

    @property
    def xbrl_zip_path(self):
        return self.__xbrl_zip_path.as_posix()

    @xbrl_zip_path.setter
    def xbrl_zip_path(self, xbrl_zip_path):
        self.__xbrl_zip_path = Path(xbrl_zip_path)

    @property
    def directory_path(self):
        return self.__directory_path

    @property
    def xbrl_type(self):
        return self.__xbrl_type

    # zipファイルを解凍するメソッドを追加して解凍したファイルのパスを返す
    def __unzip_xbrl(self) -> str:
        zip_path = Path(self.xbrl_zip_path)
        with zipfile.ZipFile(zip_path.as_posix(), 'r') as z:
            # zipファイルを解凍するパスを指定
            unzip_path = zip_path.parent / zip_path.stem
            z.extractall(unzip_path.as_posix())
        return unzip_path.as_posix()

    def __xbrl_type(self):
        directory_path = Path(self.directory_path)
        # ファイルの末尾が「ixbrl.htm」のファイルを再起的に取得してリストに追加
        ixbrl_files = list(directory_path.rglob("*ixbrl.htm"))
        if len(ixbrl_files) == 1:
            return ixbrl_files[0].as_posix().split("-")[1]
        elif len(ixbrl_files) > 1:
            for ixbrl_file in ixbrl_files:
                if "sm" in ixbrl_file.as_posix():
                    return ixbrl_file.as_posix().split("-")[1][2:6]
            raise NotXbrlDirectoryException("ixbrlファイルが複数存在します。")
        else:
            raise NotXbrlDirectoryException("ixbrlファイルが存在しません。")