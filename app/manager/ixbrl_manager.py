from pandas import DataFrame

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
        def get_value(value_: dict[str, str], item: list[str]):
            return (
            value_["numeric"]
            if any(value_["name"].endswith(item) for item in item)
            else None
            )
        contexts = []
        dfs = []
        summary = IxSummary()
        for values in self.get_ix_non_fraction("sm"):
            dfs.append(DataFrame(values))
            # dfをcontext_period, context_entity, context_categoryでグループ化
            for key, values in DataFrame(values).groupby(["context_period", "context_entity", "context_category"]):
                context = key
                contexts.append(context)
        contexts = list(set(contexts))

        for context in contexts:
            for df in dfs:
                df_query:DataFrame = df.query("context_period == @context[0] & context_entity == @context[1] & context_category == @context[2]")
                # df_queryからnameが"_NetSales"で終わる行を取得
                # 売上高
                net_sales = get_value(df_query.to_dict(orient="records")[0], ["_NetSales"])
                # 営業利益
                operating_income = get_value(df_query.to_dict(orient="records")[0], ["OperatingIncome"])
                # 経常利益
                ordinary_income = get_value(df_query.to_dict(orient="records")[0], ["_OrdinaryIncome"])
                # 純利益
                net_income = get_value(df_query.to_dict(orient="records")[0], ["_NetIncome"])
                yield net_sales, operating_income, ordinary_income, net_income
