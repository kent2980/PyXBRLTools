from app.exception import XbrlListEmptyError
from app.manager import BaseXbrlManager
from app.parser import IxbrlParser
from app.tag import IxHeader


class IXBRLManager(BaseXbrlManager):
    """iXBRLデータの解析を行うクラス

    raise   - XbrlListEmptyError("ixbrlファイルが見つかりません。")
    """

    def __init__(self, directory_path, xbrl_id:str=None) -> None:
        """
        IxbrlManagerクラスのコンストラクタです。

        Parameters:
            directory_path (str): XBRLファイルが格納されているディレクトリのパス

        Returns:
            None
        """
        super().__init__(directory_path, xbrl_id=xbrl_id)
        self.set_htmlbase_files("ixbrl")

        if len(self.files) == 0:
            raise XbrlListEmptyError("ixbrlファイルが見つかりません。")

        # items
        self.__ix_non_fraction = None
        self.__ix_non_numeric = None
        self.__ix_context = None
        self.__ix_header = None

        self.set_ix_header()
        self.set_source_file(self.xbrl_id)
        self.set_ix_non_fraction()
        self.set_ix_non_numeric()
        self.set_ix_context()

    @property
    def ix_non_fraction(self):
        return self.__ix_non_fraction

    @property
    def ix_non_numeric(self):
        return self.__ix_non_numeric

    @property
    def ix_context(self):
        return self.__ix_context

    @property
    def ix_header(self):
        return self.__ix_header

    def ix_non_fraction_yields(self):
        for value in self.ix_non_fraction:
            yield value

    def ix_non_numeric_yields(self):
        for value in self.ix_non_numeric:
            yield value

    def ix_context_yields(self):
        for value in self.ix_context:
            yield value

    def ixbrl_roles(self):
        for _, row in self.files.iterrows():
            if row["xlink_href"].endswith("ixbrl.htm"):
                parser = IxbrlParser.create(row["xlink_href"])
                yield parser.ixbrl_role

    def set_ix_non_fraction(self, document_type=None):
        """
        ix_non_fraction属性を設定します。
        非分数のIXBRLデータを取得します。

        Yields:
            dict: 非分数のIXBRLデータ
        """

        rows = []

        files = self.files

        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")

        for _, row in files.iterrows():
            if row["xlink_href"].endswith("ixbrl.htm"):

                parser = IxbrlParser.create(
                    row["xlink_href"]
                ).ix_non_fraction()

                df = parser.to_DataFrame()

                df["xbrl_id"] = self.xbrl_id

                rows.append(df.to_dict(orient="records"))

        self.__ix_non_fraction = rows

        self.items["non_fraction"] = rows

    def set_ix_non_numeric(self, document_type=None):
        """
        ix_non_numeric属性を設定します。
        非数値のIXBRLデータを取得します。

        Yields:
            dict: 非数値のIXBRLデータ
        """

        rows = []

        files = self.files

        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")

        for _, row in files.iterrows():
            if row["xlink_href"].endswith("ixbrl.htm"):

                parser = IxbrlParser.create(
                    row["xlink_href"]
                ).ix_non_numeric()

                df = parser.to_DataFrame()

                df["xbrl_id"] = self.xbrl_id

                rows.append(df.to_dict(orient="records"))

        self.__ix_non_numeric = rows

        self.items["non_numeric"] = rows

    def set_ix_context(self, document_type=None):
        """
        ix_context属性を設定します。
        iXBRLのコンテキスト情報を取得します。

        Yields:
            dict: iXBRLのコンテキスト情報
        """

        rows = []

        files = self.files

        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")

        for _, row in files.iterrows():
            if row["xlink_href"].endswith("ixbrl.htm"):

                parser = IxbrlParser.create(
                    row["xlink_href"]
                ).ix_context()

                df = parser.to_DataFrame()

                df["xbrl_id"] = self.xbrl_id

                rows.append(df.to_dict(orient="records"))

        self.__ix_context = rows

        self.items["context"] = rows

    def set_ix_header(self):
        """
        ix_header属性を設定します。
        iXBRLのヘッダー情報を取得します。

        Returns:
            self (IxbrlManager): 自身のインスタンス
        """
        header = {
            "company_name": None,
            "securities_code": None,
            "document_name": None,
            "reporting_date": None,
            "current_period": None,
            "xbrl_id": None,
            "report_type": None,
        }
        if self.ix_non_numeric is None:
            self.set_ix_non_numeric()
        for values in self.ix_non_numeric:
            for value in values:
                header["company_name"] = (
                    value["value"]
                    if any(
                        item in value["name"]
                        for item in [
                            "CompanyName",
                            "AssetManagerREIT",
                        ]
                    )
                    else header["company_name"]
                )
                header["securities_code"] = (
                    value["value"]
                    if any(
                        item in value["name"]
                        for item in ["SecuritiesCode", "SecurityCode"]
                    )
                    else header["securities_code"]
                )
                header["document_name"] = (
                    value["value"]
                    if any(
                        value["name"].endswith(item)
                        for item in ["DocumentName"]
                    )
                    else header["document_name"]
                )
                items = [
                    "FilingDate",
                    "ReportingDateOfFinancialForecastCorrection",
                    "ReportingDateOfDividendForecastCorrection",
                    "ReportingDateOfDistributionForecastCorrectionREIT",
                ]
                header["reporting_date"] = (
                    value["value"]
                    if any(value["name"].endswith(item) for item in items)
                    else header["reporting_date"]
                )
                header["current_period"] = (
                    value["value"]
                    if any(
                        item in value["name"]
                        for item in ["TypeOfCurrentPeriod"]
                    )
                    else header["current_period"]
                )
                header["xbrl_id"] = value["xbrl_id"]
                header["report_type"] = value["report_type"]

        ix_header = IxHeader(
            company_name=header["company_name"],
            securities_code=header["securities_code"],
            document_name=header["document_name"],
            reporting_date=header["reporting_date"],
            current_period=header["current_period"],
            xbrl_id=header["xbrl_id"],
            report_type=header["report_type"],
        )

        self.__ix_header = ix_header.__dict__

        self.items["header"] = ix_header.__dict__
