from app.exception import XbrlListEmptyError
from app.manager import BaseXbrlManager
from app.parser import IxbrlParser
from app.tag import IxHeader, IxSummary


class IXBRLManager(BaseXbrlManager):
    """iXBRLデータの解析を行うクラス"""

    def __init__(self, directory_path) -> None:
        """
        IxbrlManagerクラスのコンストラクタです。

        Parameters:
            directory_path (str): XBRLファイルが格納されているディレクトリのパス

        Returns:
            None
        """
        super().__init__(directory_path)
        self.set_htmlbase_files("ixbrl")

        if len(self.files) == 0:
            raise XbrlListEmptyError("ixbrlファイルが見つかりません。")

    def get_ix_non_fraction(self, document_type=None):
        """
        ix_non_fraction属性を設定します。
        非分数のIXBRLデータを取得します。

        Yields:
            dict: 非分数のIXBRLデータ
        """
        files = self.files

        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")

        for _, row in files.iterrows():
            if row["xlink_href"].endswith("ixbrl.htm"):

                parser = IxbrlParser.create(row["xlink_href"]).ix_non_fractions()

                df = parser.to_DataFrame()

                df["xbrl_id"] = self.xbrl_id

                yield df.to_dict(orient="records")

    def get_ix_non_numeric(self, document_type=None):
        """
        ix_non_numeric属性を設定します。
        非数値のIXBRLデータを取得します。

        Yields:
            dict: 非数値のIXBRLデータ
        """
        files = self.files

        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")

        for _, row in files.iterrows():
            if row["xlink_href"].endswith("ixbrl.htm"):

                parser = IxbrlParser.create(row["xlink_href"]).ix_non_numeric()

                df = parser.to_DataFrame()

                df["xbrl_id"] = self.xbrl_id

                yield df.to_dict(orient="records")

    def get_ix_header(self):
        """
        ix_header属性を設定します。
        iXBRLのヘッダー情報を取得します。

        Returns:
            self (IxbrlManager): 自身のインスタンス
        """
        company_name = None
        securities_code = None
        document_name = None
        reporting_date = None
        current_period = None
        xbrl_id = None
        report_type = None
        for values in self.get_ix_non_numeric():
            for value in values:
                if value["value"]:
                    print(f"{value['name']} : {value['value']}")
                company_name = (
                    value["value"]
                    if any(item in value["name"] for item in ["CompanyName", "AssetManagerREIT"])
                    else company_name
                )
                securities_code = (
                    value["value"]
                    if any(item in value["name"] for item in ["SecuritiesCode", "SecurityCode"])
                    else securities_code
                )
                document_name = (
                    value["value"]
                    if any(value["name"].endswith(item) for item in ["DocumentName"])
                    else document_name
                )
                reporting_date = (
                    value["value"]
                    if any(value["name"].endswith(item) for item in [
                        "FilingDate","ReportingDateOfFinancialForecastCorrection","ReportingDateOfDividendForecastCorrection","ReportingDateOfDistributionForecastCorrectionREIT"
                    ])
                    else reporting_date
                )
                current_period = (
                    value["value"]
                    if any(item in value["name"] for item in ["TypeOfCurrentPeriod"])
                    else current_period
                )
                xbrl_id = value["xbrl_id"]
                report_type = value["report_type"]

        header = IxHeader(
            company_name=company_name,
            securities_code=securities_code,
            document_name=document_name,
            reporting_date=reporting_date,
            current_period=current_period,
            xbrl_id=xbrl_id,
            report_type=report_type,
        )

        return header.__dict__

    def get_ix_summary(self):
        summary_list = []
        summary = IxSummary()
        for values in self.get_ix_non_fraction("sm"):
            for value in values:
                context_period = value["context_period"]
                context_entity = value["context_entity"]
                context_category = value["context_category"]
                net_sales = (
                    value["numeric"]
                    if any(value["name"].endswith(item) for item in ["_NetSales"])
                    else None
                )

                if net_sales:
                    value_summary = IxSummary(
                        context_period=context_period,
                        context_entity=context_entity,
                        context_category=context_category,
                        net_sales=net_sales,
                    )
                    if not summary.__eq__(value_summary):
                        summary = value_summary
                        summary_list.append(summary.__dict__)
                        context_period = None
                        context_entity = None
                        context_category = None
                        net_sales = None

        # Remove duplicates
        summary_list = summary_list[1:]
        for value in summary_list:
            yield value
