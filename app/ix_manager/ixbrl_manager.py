import re
from typing import List, Optional

from app.exception import XbrlListEmptyError
from app.exception.xbrl_parser_exception import (
    DocumentNameTagNotFoundError,
)
from app.ix_manager import BaseXbrlManager
from app.ix_parser import IxbrlParser
from app.ix_tag import IxContext, IxHeader, IxNonFraction, IxNonNumeric


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

        if len(self.related_files) == 0:
            raise XbrlListEmptyError("ixbrlファイルが見つかりません。")

        # プロパティの初期化
        self.__ix_non_fraction = None
        self.__ix_non_numeric = None
        self.__ix_context = None
        self.__ix_header = None

        # 初期化メソッドを実行
        self.__init_parser()
        self.__init_manager()
        self._set_source_file_ids()

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
        for _, row in self.related_files.iterrows():
            try:
                parser = IxbrlParser(
                    row["xlink_href"], xbrl_id=self.xbrl_id
                )
                parsers.append(parser)
            except DocumentNameTagNotFoundError:
                # 後でエラーログを出力する処理を追加するために注釈を追加
                # logger.error(f"DocumentNameタグが見つかりません。[xbrl_id]: {self.xbrl_id}")
                pass

        self._set_parsers(parsers)

    def __init_manager(self):
        """managerを初期化します。"""
        self.__set_ix_header()
        self.set_source_file(self.parsers, class_name="ix")
        self.__set_ix_non_fraction()
        self.__set_ix_non_numeric()
        self.__set_ix_context()

        self.items.sort(key=lambda x: x["sort_position"])

    def __set_ix_non_fraction(self):
        """
        ix_non_fraction属性を設定します。
        非分数のIXBRLデータを取得します。

        Yields:
            dict: 非分数のIXBRLデータ
        """

        rows: List[List[IxNonFraction]] = []

        for parser in self.parsers:

            id = parser.source_file_id

            parser: IxbrlParser = parser.set_ix_non_fraction()

            data = parser.data

            rows.append(data)

            self._set_items(id=id, key="ix_non_fraction", items=data)

        self.__ix_non_fraction = rows

    def __set_ix_non_numeric(self):
        """
        ix_non_numeric属性を設定します。
        非数値のIXBRLデータを取得します。

        Yields:
            dict: 非数値のIXBRLデータ
        """

        # ix_non_numericが設定されている場合は、何もしない
        if self.ix_non_numeric:
            return None

        rows: List[List[IxNonNumeric]] = []

        for parser in self.parsers:

            id = parser.source_file_id

            data = parser.set_ix_non_numeric()

            data = parser.data

            rows.append(data)

            self._set_items(id=id, key="ix_non_numeric", items=data)

        self.__ix_non_numeric = rows

    def __set_ix_context(self):
        """
        ix_context属性を設定します。
        iXBRLのコンテキスト情報を取得します。

        Yields:
            dict: iXBRLのコンテキスト情報
        """

        rows: List[List[IxContext]] = []

        for parser in self.parsers:

            id = parser.source_file_id

            parser = parser.set_ix_context()

            data = parser.data

            rows.append(data)

            self._set_items(id=id, key="ix_context", items=data)

        self.__ix_context = rows

    def __set_ix_header(self):
        """ix_header属性を設定します。"""

        # 変数を初期化
        company_name = None
        securities_code = None
        document_name = None
        reporting_date = None
        current_period = None
        listed_market = None
        market_section = None
        url = None
        is_bs = False
        is_pl = False
        is_cf = False
        is_ci = False
        is_sce = False
        is_sfp = False
        fiscal_year_end = None
        tel = None
        xbrl_id = None
        report_type = None

        # ix_non_numericがNoneの場合は、ix_non_numericを設定する
        if self.ix_non_numeric is None:
            self.__set_ix_non_numeric()

        for items in self.ix_non_numeric:
            for item in items:
                if re.search(
                    r"CompanyName|AssetManagerREIT", item.name
                ):  # 会社名
                    company_name = item.value
                elif re.search(r"Securit.*Code$", item.name):  # 証券コード
                    securities_code = item.value
                elif re.search(r"DocumentName", item.name):  # 書類名
                    document_name = item.value
                elif re.search(
                    r"_FilingDate$|_ReportingDateOf.*Correction.*",
                    item.name,
                ):  # 提出日
                    reporting_date = item.value
                elif re.search(r"TypeOfCurrentPeriod", item.name):  # 期間
                    current_period = item.value
                elif re.search(
                    r"TokyoStockExchange$", item.name
                ):  # 上場市場
                    if (
                        item.format == "booleantrue"
                        or item.value == "true"
                    ):
                        listed_market = "東京証券取引所"
                elif re.search(
                    r"TokyoStockExchange(?!$)", item.name
                ):  # 上場区分
                    if (
                        item.format == "booleantrue"
                        or item.value == "true"
                    ):
                        market_section = item.name
                elif re.search(r".*URL.*", item.name):  # URL
                    url = item.value
                elif re.search(
                    r".*BalanceSheet.*TextBlock$", item.name
                ):  # 貸借対照表の存在フラグ
                    is_bs = True
                elif re.search(
                    r"(.*StatementOfIncome|.*StatementOfProfitOrLoss).*TextBlock$",
                    item.name,
                ):  # 損益計算書の存在フラグ
                    is_pl = True
                elif re.search(
                    r".*StatementOfCashFlows.*TextBlock$", item.name
                ):  # キャッシュフロー計算書の存在フラグ
                    is_cf = True
                elif re.search(
                    r".*StatementOfComprehensiveIncome.*TextBlock$",
                    item.name,
                ):  # 包括利益計算書の存在フラグ
                    is_ci = True
                elif re.search(
                    r".*StatementOfChangesInEquity.*TextBlock$", item.name
                ):  # 株主資本変動計算書の存在フラグ
                    is_sce = True
                elif re.search(
                    r".*StatementOfFinancialPositionI.*TextBlock$",
                    item.name,
                ):  # 財政状態計算書の存在フラグ
                    is_sfp = True
                elif re.search(r".*FiscalYearEnd$", item.name):  # 決算期
                    fiscal_year_end = item.value
                elif re.search(r".*Tel$", item.name):  # 電話番号
                    tel = item.value
                xbrl_id = item.xbrl_id  # XBRL ID
                report_type = item.report_type  # 提出種別

        ix_header = IxHeader(
            company_name=company_name,
            securities_code=securities_code,
            document_name=document_name,
            reporting_date=reporting_date,
            current_period=current_period,
            xbrl_id=xbrl_id,
            report_type=report_type,
            listed_market=listed_market,
            market_section=market_section,
            url=url,
            is_bs=is_bs,
            is_pl=is_pl,
            is_cf=is_cf,
            is_ci=is_ci,
            is_sce=is_sce,
            is_sfp=is_sfp,
            fiscal_year_end=fiscal_year_end,
            tel=tel,
        )

        header = ix_header

        self.__ix_header = header

        self._set_items(
            id=ix_header.xbrl_id,
            key="ix_head_title",
            items=header,
            sort_position=0,
        )
