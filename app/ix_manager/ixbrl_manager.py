from typing import List, Optional

from app.exception import XbrlListEmptyError
from app.ix_manager import BaseXbrlManager
from app.ix_parser import IxbrlParser
from app.ix_tag import IxHeader


class IXBRLManager(BaseXbrlManager):
    """iXBRLデータの解析を行うクラス

    raise   - XbrlListEmptyError("ixbrlファイルが見つかりません。")
    """

    def __init__(
        self, directory_path, xbrl_id: Optional[str] = None
    ) -> None:
        """
        IxbrlManagerクラスのコンストラクタです。

        Parameters:
            directory_path (str): XBRLファイルが格納されているディレクトリのパス

        Returns:
            None
        """
        super().__init__(directory_path, xbrl_id=xbrl_id)
        self._set_htmlbase_files("ixbrl")

        if len(self.files) == 0:
            raise XbrlListEmptyError("ixbrlファイルが見つかりません。")

        # プロパティの初期化
        self.__parsers: Optional[List[IxbrlParser]] = None
        self.__ix_non_fraction = None
        self.__ix_non_numeric = None
        self.__ix_context = None
        self.__ix_header = None

        # 初期化メソッドを実行
        self.__init_parser()
        self.__init_manager()

    @property
    def parsers(self):
        return self.__parsers

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

    def __init_parser(self):
        """parserを初期化します。"""
        parsers: List[IxbrlParser] = []
        for _, row in self.files.iterrows():
            parser = IxbrlParser(row["xlink_href"], xbrl_id=self.xbrl_id)
            parsers.append(parser)

        self.__parsers = parsers

    def __init_manager(self):
        """managerを初期化します。"""
        self.set_source_file(self.parsers)
        self.__set_ix_header()
        self.__set_ix_non_fraction()
        self.__set_ix_non_numeric()
        self.__set_ix_context()

    def __set_ix_non_fraction(self):
        """
        ix_non_fraction属性を設定します。
        非分数のIXBRLデータを取得します。

        Yields:
            dict: 非分数のIXBRLデータ
        """

        rows = []

        for parser in self.parsers:

            parser = parser.set_ix_non_fraction()

            data = parser.data

            rows.append(data)

        self.__ix_non_fraction = rows

        self._set_items("non_fraction", rows)

    def __set_ix_non_numeric(self):
        """
        ix_non_numeric属性を設定します。
        非数値のIXBRLデータを取得します。

        Yields:
            dict: 非数値のIXBRLデータ
        """

        rows = []

        for parser in self.parsers:

            data = parser.set_ix_non_numeric()

            data = parser.data

            rows.append(data)

        self.__ix_non_numeric = rows

        self._set_items("non_numeric", rows)

    def __set_ix_context(self):
        """
        ix_context属性を設定します。
        iXBRLのコンテキスト情報を取得します。

        Yields:
            dict: iXBRLのコンテキスト情報
        """

        rows = []

        for parser in self.parsers:

            parser = parser.set_ix_context()

            data = parser.data

            rows.append(data)

        self.__ix_context = rows

        self._set_items("context", rows)

    def __set_ix_header(self):
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
            self.__set_ix_non_numeric()
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
                # header["source_file_id"] = value["source_file_id"]

        ix_header = IxHeader(
            company_name=header["company_name"],
            securities_code=header["securities_code"],
            document_name=header["document_name"],
            reporting_date=header["reporting_date"],
            current_period=header["current_period"],
            xbrl_id=header["xbrl_id"],
            report_type=header["report_type"],
            # source_file_id=header["source_file_id"],
        )

        self.__ix_header = ix_header.__dict__

        self._set_items("header", ix_header.__dict__)
