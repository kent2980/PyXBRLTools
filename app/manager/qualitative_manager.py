import pandas

from app.exception import XbrlListEmptyError
from app.manager import BaseXbrlManager
from app.parser import QualitativeParser


class QualitativeManager(BaseXbrlManager):
    """qualitativeデータの解析を行うクラス

    raise   - XbrlListEmptyError("qualitative.htmが見つかりません。")
    """

    def __init__(self, directory_path) -> None:
        super().__init__(directory_path)
        self.set_htmlbase_files("qualitative")

        if len(self.files) == 0:
            raise XbrlListEmptyError("qualitative.htmが見つかりません。")

    def qualitative_infos(self, document_type=None):
        df = None

        if document_type is not None:
            files = self.files.query(f"document_type == '{document_type}'")

        for index, row in files.iterrows():
            parser = QualitativeParser.create(row["xlink_href"])
            if df is None:
                df = parser.qualitative_info().to_DataFrame()
            else:
                df = pandas.concat(
                    [df, parser.qualitative_info().to_DataFrame()],
                    ignore_index=True,
                )

        self.data = df.to_dict(orient="records")

        return self
