import os
import re
from urllib.parse import urlparse

from app.exception import TypeOfXBRLIsDifferent
from app.tag import IxNonFraction, IxNonNumeric
from app.utils import Utils

from . import BaseXBRLParser


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

    Examples:
        >>> from xbrl_parser.ixbrl_parser import IxbrlParser
        >>> parser = IxbrlParser.create(file_path)
        >>> print(parser.ix_non_numeric().to_dataframe())
    """

    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path)
        # ファイルの拡張子がixbrl.htmでない場合はエラーを出力
        if not self.basename().endswith("ixbrl.htm"):
            raise TypeOfXBRLIsDifferent(
                f"{self.basename()} はixbrl.htmではありません。"
            )
        # ドキュメントの種類を設定
        self.document = self._set_document(xbrl_url)
        self.report_type = self._set_report_type(xbrl_url)

    def _set_document(self, xbrl_url):
        """ドキュメントの種類を設定する"""
        if xbrl_url.startswith("http"):
            parse_url = urlparse(xbrl_url)
            file_name = os.path.basename(parse_url.path)
        else:
            file_name = os.path.basename(xbrl_url)
        if "fr" in file_name:
            return file_name.split("-")[1][2:4]
        else:
            return "sm"

    def _set_report_type(self, xbrl_url):
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

    def ix_non_numeric(self):
        """iXBRLの非数値情報を取得する

        Returns:
            self: IxbrlParser
        """

        lists = []

        tags = self.soup.find_all(name="ix:nonNumeric")

        for tag in tags:

            # _____attr[contextRef]
            context_parts = tag.get("contextRef").split("_")
            context_period = context_parts[0]
            context_entity = context_parts[1] if len(context_parts) > 1 else None
            context_category = context_parts[2] if len(context_parts) > 2 else None

            # _____attr[xsi:nil]
            xsi_nil = True if tag.get("xsi:nil") == "true" else False

            # _____attr[escape]
            escape = True if tag.get("escape") == "true" else False

            # _____attr[name]
            name = tag.get("name").replace(":", "_")

            # _____attr[text]
            if escape == False:
                # text属性が存在する場合は取得
                text = tag.text.splitlines()[0].replace("　", "").replace(" ", "")
                # textの数字を半角に変換
                text = re.sub(r"[０-９]", lambda x: chr(ord(x.group(0)) - 0xFEE0), text)
            else:
                text = None

            format_str = tag.get("format").split(":")[-1] if tag.get("format") else None

            # textが日付文字列の場合はフォーマットを統一
            if format_str:
                text, format_str = Utils.date_str_to_format(text, format_str)   # pragma: no cover

            # textが証券コードの場合は4文字に統一
            if "SecuritiesCode" in name:
                text = text[0:4]  # pragma: no cover

            # 辞書に追加
            inn = IxNonNumeric(
                xbrl_id=self.xbrl_id,
                context_period=context_period,
                context_entity=context_entity,
                context_category=context_category,
                name=name,
                xsi_nil=xsi_nil,
                escape=escape,
                format=format_str,
                value=text,
                document_type=self.document,
                report_type=self.report_type,
            )
            lists.append(inn.__dict__)

        self.data = lists

        return self

    def ix_non_fractions(self):
        """iXBRLの非分数情報を取得する

        Returns:
            self: IxbrlParser
        """
        # ix_non_fractionが存在する場合はそのまま返す

        lists = []
        tags = self.soup.find_all(name="ix:nonFraction")
        for tag in tags:
            # _____attr[contextRef]
            context_parts = tag.get("contextRef").split("_")
            context_period = context_parts[0]
            context_entity = context_parts[1] if len(context_parts) > 1 else None
            context_category = context_parts[2] if len(context_parts) > 2 else None

            # _____attr[decimals]
            decimals = int(tag.get("decimals")) if tag.get("decimals") else None

            # _____attr[format]
            format_str = tag.get("format").split(":")[-1] if tag.get("format") else None

            # _____attr[name]
            name = tag.get("name").replace(":", "_")

            # _____attr[scale]
            scale = int(tag.get("scale")) if tag.get("scale") else None

            # _____attr[sign]
            sign = tag.get("sign")

            # _____attr[unitRef]
            unit_ref = tag.get("unitRef")

            # _____attr[xsi:nil]
            xsi_nil = True if tag.get("xsi:nil") == "true" else False

            # _____attr[numeric]
            numeric = int(re.sub(",", "", tag.text)) if tag.text else None
            numeric = numeric * -1 if sign == "-" else numeric

            inn = IxNonFraction(
                xbrl_id=self.xbrl_id,
                context_period=context_period,
                context_entity=context_entity,
                context_category=context_category,
                decimals=decimals,
                format=format_str,
                name=name,
                scale=scale,
                unit_ref=unit_ref,
                xsi_nil=xsi_nil,
                numeric=numeric,
                document_type=self.document,
                report_type=self.report_type,
            )
            lists.append(inn.__dict__)

        self.data = lists

        return self
