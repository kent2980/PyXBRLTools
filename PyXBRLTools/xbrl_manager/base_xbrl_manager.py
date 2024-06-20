from pathlib import Path
from PyXBRLTools.xbrl_parser.schema_parser import SchemaParser
import pandas as pd
from pandas import DataFrame
from PyXBRLTools.xbrl_exception.xbrl_manager_exception import XbrlDirectoryNotFoundError

class BaseXbrlManager:
    """XBRLディレクトリの解析を行う基底クラス"""

    REPORT_TYPE = {
        "edjp": "決算短信(日本基準)",
        "edus": "決算短信(米国基準)",
        "edif": "決算短信(国際会計基準)",
        "edit": "決算短信(国際会計基準)",
        "rvdf": "配当予想修正に関するお知らせ",
        "rvfc": "業績予想修正に関するお知らせ",
        "rejp": "REIT決算短信(日本基準)",
        "rrdf": "分配予想の修正に関するお知らせ",
        "rrfc": "運用状況の予想の修正に関するお知らせ",
        "efjp": "ETF決算短信(日本基準)"
    }

    def __init__(self, directory_path) -> None:
        self.directory_path = Path(directory_path)
        self.files = None
        self.data:DataFrame|None = None

    @property
    def directory_path(self):
        return self.__directory_path

    @directory_path.setter
    def directory_path(self, directory_path):
        directory_path = Path(directory_path)
        if not directory_path.exists():
            raise XbrlDirectoryNotFoundError(f"無効なパス[{directory_path} ]")
        self.__directory_path = directory_path

    def __to_filelist(self):
        """ディレクトリ内のファイル一覧を取得する

        Returns:
            list: ファイル一覧
        """
        return [file.as_posix()
                for file in self.directory_path.glob("**/*")
                if file.is_file() and not file.name.startswith(".")]

    def xbrl_type(self):
        """書類品種を取得します

        Returns:
            tuple: 書類品種 (品種コード, 書類名)

        Examples:
            >>> manager = BaseXbrlManager("path/to/directory")
            >>> type_str, report_type = manager.xbrl_type()
            >>> print(f'1.{type_str}')
            >>> print(f'2.{report_type}')
            [output]
            1.edjp
            2.決算短信(日本基準)
        """
        files = self.__to_filelist()
        for file_str in files:
            file = Path(file_str)
            if file.suffix == '.xsd' and "fr" not in file.name:
                type_str = file.name.split("-")[1]
                code = type_str[:4] if len(type_str) == 4 else type_str[2:6]
                return code, self.REPORT_TYPE.get(code)

    def set_linkbase_files(self, xlink_role=None):
        """関係ファイルのリストを取得する

        Returns:
            pd.DataFrame: 関係ファイルのデータフレーム
        """
        files = self.__to_filelist()
        xsd_files = [file for file in files if Path(file).suffix == '.xsd']

        data_frames = [SchemaParser.create(file).link_base_refs().to_DataFrame() for file in xsd_files]
        df = pd.concat(data_frames, ignore_index=True)

        href_map = {row["xlink_href"]: file
                    for file in files
                    for index, row in df.iterrows()
                    if not row["xlink_href"].startswith('http') and row["xlink_href"] in file}

        df["xlink_href"] = df["xlink_href"].astype(str).apply(lambda href: href_map.get(href, href))

        # dfのxlink_roleカラムを整形
        df["xlink_role"] = df["xlink_role"].apply(lambda role: role.split("/")[-1] if isinstance(role, str) else role)
        # dfのxlink_arcroleカラムを整形
        df["xlink_arcrole"] = df["xlink_arcrole"].apply(lambda arcrole: arcrole.split("/")[-1] if isinstance(arcrole, str) else arcrole)

        if xlink_role:
            query = f"xlink_role == '{xlink_role}'"
            df = df.query(query)
        print(xlink_role)
        print(df)
        self.files = df
        return self

    def set_htmlbase_files(self, xlink_role=None):
        """ HTMLベースのファイルリストを取得する

        Returns:
            pd.DataFrame: HTMLベースのファイルリスト
        """
        lists = []
        files = self.__to_filelist()
        for file_str in files:
            file = Path(file_str)
            if file.suffix == '.htm' or file.suffix == '.html':
                document_type = file.name.split('-')[1][2:4] if "fr" in file.name else "sm"
                lists.append({
                    'xlink_type': 'simple',
                    'xlink_href': file.as_posix(),
                    'xlink_role': f"{file.name.split('-')[-1].split('.')[0]}",
                    'xlink_arcrole': "htmlbase",
                    'document_type': document_type,
                })

        df = pd.DataFrame(lists)

        if xlink_role:
            query = f"xlink_role == '{xlink_role}'"
            df = df.query(query)

        self.files = df

        return self

    def to_csv(self, file_path):
        """ CSV形式で出力する """
        df = DataFrame(self.data)
        df.to_csv(file_path, index=False)

    def to_DataFrame(self):
        """ DataFrame形式で出力する """
        return DataFrame(self.data)

    def to_json(self, file_path):
        """ JSON形式で出力する """
        df = DataFrame(self.data)
        df.to_json(file_path, orient='records', lines=True)

    def to_dict(self):
        """ 辞書形式で出力する """
        return self.data
