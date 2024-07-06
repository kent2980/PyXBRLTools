import os
import re
from urllib.parse import urlparse

from datetimejp import JDate

from app.exception import TypeOfXBRLIsDifferent

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
        self.document = self.__set_document(xbrl_url)
        self.report_type = self.__set_report_type(xbrl_url)

        self.__ix_non_fraction = None
        self.__ix_non_numeric = None

    def __set_document(self, xbrl_url):
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

    def ix_non_numeric(self):
        """iXBRLの非数値情報を取得する

        Returns:
            self: IxbrlParser

        Examples:
            >>> parser = IxbrlParser.create(file_path)
            >>> print(parser.ix_non_numeric().to_DataFrame())
            [output]:
            context_period: CurrentYearDuration
            context_entity: ConsolidatedMember
            context_category: ResultMember
            name: tse-ed-t_FilingDate
            xsi_nil: False
            escape: False
            format: dateyearmonthdaycjk
            text: 2024年6月13日
        """
        # ix_non_numericが存在する場合はそのまま返す

        lists = []
        tags = self.soup.find_all(name="ix:nonNumeric")
        for tag in tags:

            # xsi:nil属性が存在する場合はTrueに設定
            xsi_nil = True if tag.get("xsi:nil") == "true" else False
            # escape属性が存在する場合はTrueに設定
            escape = True if tag.get("escape") == "true" else False

            # text属性が存在する場合は取得
            text = (
                tag.text.splitlines()[0].replace("　", "").replace(" ", "")
                if tag.text
                else None
            )
            # textの数字を半角に変換
            text = (
                re.sub(r"[０-９]", lambda x: chr(ord(x.group(0)) - 0xFEE0), text)
                if text
                else None
            )

            format_str = tag.get("format").split(":")[-1] if tag.get("format") else None

            # 銘柄コードの場合は4文字まで取得
            if "SecuritiesCode" in tag.get("name"):
                text = text[0:4]

            # textが日付文字列の場合はフォーマットを統一
            if format_str:
                if "dateyearmonthdaycjk" in format_str:
                    # textの「yyyy年mm月dd日」を「yyyy-mm-dd」に変換
                    text = text.replace("年", "-").replace("月", "-").replace("日", "")
                    # textの数字部分を0埋め
                    text = re.sub(r"(\d+)", lambda x: x.group(0).zfill(2), text)
                    format_str = "dateyearmonthday"
                elif "dateerayearmonthdayjp" in format_str:
                    jd = JDate.strptime(text, "%g%e年%m月%d日")
                    text = jd.strftime("%Y-%m-%d")
                    # textの数字部分を0埋め
                    text = re.sub(r"(\d+)", lambda x: x.group(0).zfill(2), text)
                    format_str = "dateyearmonthday"

            if text:
                # textが「yyyy-mm-dd」の場合
                if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
                    format_str = "dateyearmonthday"

            # name_spaceを取得
            name_spaces = self.name_spaces()
            name_apace = name_spaces[tag.get("name").split(":")[0]]

            # 辞書に追加
            lists.append(
                {
                    "xbrl_id": self.xbrl_id,
                    "context_period": tag.get("contextRef").split("_")[0],
                    "context_entity": (
                        tag.get("contextRef").split("_")[1]
                        if len(tag.get("contextRef").split("_")) > 1
                        else None
                    ),
                    "context_category": (
                        tag.get("contextRef").split("_")[2]
                        if len(tag.get("contextRef").split("_")) > 2
                        else None
                    ),
                    "name": tag.get("name").replace(":", "_"),
                    "xsi_nil": xsi_nil,
                    "escape": escape,
                    "format": format_str,
                    "text": text if escape == False else None,
                    "document_type": self.document,
                    "report_type": self.report_type,
                    # 'name_space': name_apace
                }
            )

        self.data = lists

        return self

    def ix_non_fractions(self):
        """iXBRLの非分数情報を取得する

        Returns:
            self: IxbrlParser

        Examples:
            >>> parser = IxbrlParser.create(file_path)
            >>> print(parser.ix_non_fractions().to_DataFrame())
            [output]:
            context_period: CurrentYearDuration
            context_entity: ConsolidatedMember
            context_category: ResultMember
            decimals: 0
            format: numdotdecimal
            name: tse-ed-t_NumberOfSharesIssued
            scale: 3
            sign: -
            unit_ref: JPN
            xsi_nil: False
            numeric: 1234
        """
        # ix_non_fractionが存在する場合はそのまま返す

        lists = []
        tags = self.soup.find_all(name="ix:nonFraction")
        for tag in tags:
            numeric = re.sub(",", "", tag.text) if tag.text else None

            # name_spaceを取得
            name_spaces = self.name_spaces()
            name_apace = name_spaces[tag.get("name").split(":")[0]]
            tag_dict = {
                "xbrl_id": self.xbrl_id,
                "context_period": tag.get("contextRef").split("_")[0],
                "context_entity": (
                    tag.get("contextRef").split("_")[1]
                    if len(tag.get("contextRef").split("_")) > 1
                    else None
                ),
                "context_category": (
                    tag.get("contextRef").split("_")[2]
                    if len(tag.get("contextRef").split("_")) > 2
                    else None
                ),
                "decimals": int(tag.get("decimals")) if tag.get("decimals") else None,
                "format": tag.get("format"),
                "name": tag.get("name").replace(":", "_"),
                "scale": int(tag.get("scale")) if tag.get("scale") else None,
                "sign": tag.get("sign"),
                "unit_ref": tag.get("unitRef"),
                "xsi_nil": True if tag.get("xsi:nil") == "true" else False,
                "numeric": numeric,
                "document_type": self.document,
                "report_type": self.report_type,
                # 'name_space': name_apace
            }
            lists.append(tag_dict)

        self.data = lists

        return self

    def name_spaces(self):
        """名前空間を取得する

        Returns:
            str: 名前空間

        Examples:
            >>> parser = IxbrlParser.create(file_path)
            >>> print(parser.name_space())
            [output]:
            http://www.xbrl.org/2003/instance
        """
        # htmlタグのxmlns:から始まる属性を全て取得
        name_spaces = {}
        tags = self.soup.find_all("html")
        for tag in tags:
            for key, value in tag.attrs.items():
                if key.startswith("xmlns:"):
                    name_spaces[key.split(":")[-1]] = value
        return name_spaces
