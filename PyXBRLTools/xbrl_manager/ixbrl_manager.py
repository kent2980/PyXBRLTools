from PyXBRLTools.xbrl_manager.base_xbrl_manager import BaseXbrlManager
from PyXBRLTools.xbrl_parser.ixbrl_parser import IxbrlParser
import pandas as pd
from PyXBRLTools.xbrl_exception.xbrl_manager_exception import XbrlListEmptyError

class IxbrlManager(BaseXbrlManager):
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
        self.ix_non_fraction = None
        self.ix_non_numeric = None
        self.ix_header = None

        if len(self.files) == 0:
            raise XbrlListEmptyError("ixbrlファイルが見つかりません。")

    def set_ix_non_fraction(self, document_type=None):
        """
        ix_non_fraction属性を設定します。
        非分数のIXBRLデータを取得します。

        Returns:
            self (IxbrlManager): 自身のインスタンス
        """
        df = None
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if row["xlink_href"].endswith(".htm"):
                if df is None:
                    df = IxbrlParser.create(row["xlink_href"]).ix_non_fractions().to_DataFrame()
                else:
                    df = pd.concat([df, IxbrlParser.create(row["xlink_href"]).ix_non_fractions().to_DataFrame()], ignore_index=True)

        df['xbrl_id'] = self.xbrl_id
        self.ix_non_fraction = df.to_dict(orient="records")
        self.data = self.ix_non_fraction

        return self

    def set_ix_non_numeric(self, document_type=None):
        """
        ix_non_numeric属性を設定します。
        非数値のIXBRLデータを取得します。

        Returns:
            self (IxbrlManager): 自身のインスタンス
        """
        df = None
        files:pd.DataFrame = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if df is None:
                df = IxbrlParser.create(row["xlink_href"]).ix_non_numeric().to_DataFrame()
            else:
                df = pd.concat([df, IxbrlParser.create(row["xlink_href"]).ix_non_numeric().to_DataFrame()], ignore_index=True)

        df['xbrl_id'] = self.xbrl_id
        self.ix_non_numeric = df.to_dict(orient="records")
        self.data = self.ix_non_numeric

        return self

    def set_ix_header(self, document_type=None):
        """
        ix_header属性を設定します。
        iXBRLのヘッダー情報を取得します。

        Returns:
            self (IxbrlManager): 自身のインスタンス
        """
        df = self.set_ix_non_numeric().to_DataFrame()

        if document_type is not None:
            df = df.query(f"document_type == '{document_type}'")

        def extract_fields(group):
            return pd.Series({
                'company_name': group.loc[group['name'].str.contains('CompanyName|AssetManagerREIT'), 'text'].iloc[0],
                'securities_code': group.loc[group['name'].str.contains('SecuritiesCode'), 'text'].iloc[0],
                'document_name': group.loc[group['name'].str.contains('DocumentName'), 'text'].iloc[0],
                'reporting_date': group.loc[group['name'].str.contains('FilingDate|ReportingDateOfFinancialForecastCorrection|ReportingDateOfDividendForecastCorrection|ReportingDateOfDistributionForecastCorrectionREIT'), 'text'].iloc[0]
            })

        result_df = df.groupby(['xbrl_id', 'report_type']).apply(extract_fields).reset_index()

        self.data = result_df

        return self

def set_ix_summary(self):
    def get_filtered_df(df, column_name, filter_value):
        return df[df[column_name].str.contains(filter_value)].reset_index()

    # 非分数のIXBRLデータを取得
    df = self.set_ix_non_fraction().to_DataFrame()

    jpy_df = get_filtered_df(df, 'unit_ref', 'JPY')
    pure_df = get_filtered_df(df, 'unit_ref', 'Pure')
    jps_df = get_filtered_df(df, 'unit_ref', 'JPYPerShares')

    # dfからreport_typeの最初の値を取得
    report_type = df['report_type'].iloc[0]

    # 各指標名と対応するデータフレームを定義
    metrics = {
        "sales": ["NetSales", jpy_df, pure_df],
        "ope_income": ["OperatingIncome", jpy_df, pure_df],
        "ord_income": ["OrdinaryIncome", jpy_df, pure_df],
        "profit": ["NetIncome", jpy_df, pure_df],
        "profit_per_share": ["NetIncomePerShare", jps_df, None],
        "net_assets": ["NetAssets", jpy_df, pure_df],
        "net_assets_per_share": ["NetAssetsPerShare", jps_df, None],
        "dividend": ["Dividends", jpy_df, None],
        "dividend_ratio": ["DividendPayoutRatio", pure_df, None],
        "equity_ratio": ["EquityRatio", pure_df, None],
        "total_assets": ["TotalAssets", jpy_df, pure_df],
        "total_assets_per_share": ["TotalAssetsPerShare", jps_df, None],
        "total_assets_turnover": ["TotalAssetsTurnover", pure_df, None],
        "interest_bearing_debt": ["InterestBearingDebt", jpy_df, None],
        "interest_bearing_debt_ratio": ["InterestBearingDebtRatio", pure_df, None],
        "interest_bearing_debt_rate": ["InterestBearingDebtRate", pure_df, None],
        "interest_bearing_debt_period": ["InterestBearingDebtPeriod", pure_df, None]
    }

    results = {}
    for key, (name, df1, df2) in metrics.items():
        results[key] = get_filtered_df(df1, 'name', name)
        if df2 is not None:
            results[f"{key}_change"] = get_filtered_df(df2, 'name', name)

    return results
