import json
import os
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlparse

from app.exception import TypeOfXBRLIsDifferent
from app.tag import IxContext, IxNonFraction, IxNonNumeric
from app.utils import Utils

from . import BaseXBRLParser


def read_const():
    # 現在のディレクトリを取得
    current_dir = Path(os.path.dirname(__file__)).parent
    const_path = current_dir / "const" / "const.json"
    with open(const_path) as f:
        const = json.load(f)
    return const


class IxbrlParser(BaseXBRLParser):
    """iXBRLを解析するクラス
        このクラスはBaseXBRLParserを継承しています。
        iXBRLの解析を行います。
        以下の機能を提供します。
        - iXBRLの非数値情報取得
        - iXBRLの非分数情報取得

    Attributes:
    - xbrl_url: str
        XBRLのURL
    - output_path: str
        ファイルの保存先

    Properties:
    - data: list[dict]
        解析結果のデータ

    Methods:
    - ix_non_numeric
        iXBRLの非数値情報を取得する
    - ix_non_fractions
        iXBRLの非分数情報を取得する
    """

    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path)
        # ファイルの拡張子がixbrl.htmでない場合はエラーを出力
        if not self.basename.endswith("ixbrl.htm"):
            raise TypeOfXBRLIsDifferent(
                f"{self.basename} はixbrl.htmではありません。"
            )

        self.__report_type = None
        self.__ixbrl_role = None
        self.__ix_non_fraction = None
        self.__ix_non_numeric = None
        self.__ix_context = None

        # 初期化処理
        self.__init_xbrl()

    def __init_xbrl(self):
        self.__report_type = self.__set_report_type(self.xbrl_url)
        self.__ixbrl_role = self.__set_ixbrl_role()

    @property
    def report_type(self):
        return self.__report_type

    @property
    def ixbrl_role(self):
        return self.__ixbrl_role

    def __set_report_type(self, xbrl_url):
        """レポートの種類を設定する"""
        if xbrl_url.startswith("http"):
            parse_url = urlparse(xbrl_url)
            file_name = os.path.basename(parse_url.path)
        else:
            file_name = os.path.basename(xbrl_url)
        if "sm" in file_name:
            return file_name.split("-")[1][2:6]
        elif "fr" in file_name:
            return file_name.split("-")[3][2:6]
        else:
            return file_name.split("-")[1]

    def __set_ixbrl_role(self):
        """ドキュメントの要素を設定する"""
        const = read_const()
        file_name = self.basename
        ixbrl_type = file_name.split("-")[1]
        role = {}
        if "fr" not in file_name:
            role = {
                "type": "summary",
                "jp_label": "短信サマリー",
                "en_label": "FinancialReportSummary",
            }
        else:
            role = {
                "type": ixbrl_type,
                "jp_label": const["document_name"][ixbrl_type],
                "en_label": const["document_element"][ixbrl_type],
            }
        return role

    def ix_non_numeric(self):
        """iXBRLの非数値情報を取得する

        Returns:
            self: IxbrlParser
        """

        if self.__ix_non_numeric:
            self.data = self.ix_non_numeric

        lists = []

        tags = self.soup.find_all(name="ix:nonNumeric")

        for tag in tags:

            # _____attr[contextRef]
            context = tag.get("contextRef")

            # _____attr[xsi:nil]
            xsi_nil = True if tag.get("xsi:nil") == "true" else False

            # _____attr[escape]
            escape = True if tag.get("escape") == "true" else False

            # _____attr[name]
            name = tag.get("name").replace(":", "_")

            # _____attr[text]
            if escape is False:
                # text属性が存在する場合は取得
                text = tag.text.replace("　", "").replace(" ", "")
                # textの数字を半角に変換
                text = re.sub(
                    r"[０-９]",
                    lambda x: chr(ord(x.group(0)) - 0xFEE0),
                    text,
                )
            else:
                text = None

            format_str = (
                tag.get("format").split(":")[-1]
                if tag.get("format")
                else None
            )

            # textが日付文字列の場合はフォーマットを統一
            if format_str:
                text, format_str = Utils.date_str_to_format(
                    text, format_str
                )  # pragma: no cover

            # textが証券コードの場合は4文字に統一
            if any(
                item in name for item in ["SecuritiesCode", "SecurityCode"]
            ):
                text = text[0:4]  # pragma: no cover

            # textが空白の場合はNoneに変換
            if text == "":
                text = None

            # 辞書に追加
            inn = IxNonNumeric(
                xbrl_id=self.xbrl_id,
                context=context,
                name=name,
                xsi_nil=xsi_nil,
                escape=escape,
                format=format_str,
                value=text,
                report_type=self.report_type,
                ixbrl_role=self.ixbrl_role["en_label"],
            )
            lists.append(inn.__dict__)

        self._set_data(lists)

        self.__ix_non_numeric = lists

        return self

    def ix_non_fraction(self):
        """iXBRLの非分数情報を取得する

        Returns:
            self: IxbrlParser
        """
        # ix_non_fractionが存在する場合はそのまま返す

        if self.__ix_non_fraction:
            self.data = self.ix_non_fraction

        lists = []
        tags = self.soup.find_all(name="ix:nonFraction")
        for tag in tags:
            # _____attr[format]
            format_str = (
                tag.get("format").split(":")[-1]
                if tag.get("format")
                else None
            )

            # _____attr[contextRef]
            context = tag.get("contextRef")

            # _____attr[decimals]
            decimals = tag.get("decimals")

            # _____attr[name]
            name = tag.get("name").replace(":", "_")

            # _____attr[scale]
            scale = tag.get("scale")

            # _____attr[sign]
            sign = tag.get("sign")

            # _____attr[unitRef]
            unit_ref = tag.get("unitRef")

            # _____attr[xsi:nil]
            xsi_nil = True if tag.get("xsi:nil") == "true" else False

            # _____attr[numeric]
            numeric = tag.text
            if numeric is not None:
                try:
                    numeric = Decimal(re.sub(",", "", tag.text))
                    if sign == "-":
                        numeric = numeric * -1
                    numeric = str(numeric)
                except (ValueError, InvalidOperation, TypeError):
                    numeric = None

            if format_str is None:
                decimals = None
                scale = None
                numeric = None

            inn = IxNonFraction(
                xbrl_id=self.xbrl_id,
                context=context,
                decimals=decimals,
                format=format_str,
                name=name,
                scale=scale,
                unit_ref=unit_ref,
                xsi_nil=xsi_nil,
                numeric=numeric,
                report_type=self.report_type,
                ixbrl_role=self.ixbrl_role["en_label"],
            )
            lists.append(inn.__dict__)

        self._set_data(lists)

        self.__ix_non_fraction = lists

        return self

    def ix_context(self):

        if self.__ix_context:
            self.data = self.__ix_context

        lists = []
        tags = self.soup.find_all(name="xbrli:context")
        for tag in tags:
            # _____attr[id]
            context_id = tag.get("id")
            for period in tag.find_all(name="xbrli:period"):
                start, end, instant = None, None, None
                # _____attr[start]
                if period.find(name="xbrli:startDate") is not None:
                    start = period.find(name="xbrli:startDate").text
                # _____attr[end]
                if period.find(name="xbrli:endDate") is not None:
                    end = period.find(name="xbrli:endDate").text
                # _____attr[instant]
                if period.find(name="xbrli:instant") is not None:
                    instant = period.find(name="xbrli:instant").text
                period = {"start": start, "end": end, "instant": instant}
            scenario = []
            for value in tag.find_all(name="xbrli:scenario"):
                for explicit_member in value.find_all(
                    name="xbrldi:explicitMember"
                ):
                    dimension = explicit_member.get("dimension").replace(
                        ":", "_"
                    )
                    scenario_value = explicit_member.text.replace(":", "_")
                    scenario.append(
                        {"dimension": dimension, "value": scenario_value}
                    )

            inn = IxContext(
                xbrl_id=self.xbrl_id,
                context_id=context_id,
                period=period,
                scenario=scenario,
            )
            lists.append(inn.__dict__)

        self._set_data(lists)

        self.__ix_context = lists

        return self
