from .base_xbrl_parser import BaseXBRLParser
import re

class IxbrlParser(BaseXBRLParser):
    """ iXBRLを解析するクラス
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

    def ix_non_numeric(self):
        """ iXBRLの非数値情報を取得する

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
        lists = []
        tags = self.soup.find_all(name='ix:nonNumeric')
        for tag in tags:
            # xsi:nil属性が存在する場合はTrueに設定
            xsi_nil = True if tag.get('xsi:nil') == 'true' else False
            # escape属性が存在する場合はTrueに設定
            escape = True if tag.get('escape') == 'true' else False
            # text属性が存在する場合は取得
            text = tag.text.splitlines()[0].replace("　", "").replace(" ", "") if tag.text else None
            # 辞書に追加
            lists.append({
                'context_period': tag.get('contextRef').split("_")[0],
                'context_entity': tag.get('contextRef').split("_")[1] if len(tag.get('contextRef').split("_")) > 1 else None,
                'context_category': tag.get('contextRef').split("_")[2] if len(tag.get('contextRef').split("_")) > 2 else None,
                'name': tag.get('name').replace(":", "_"),
                'xsi_nil': xsi_nil,
                'escape': escape,
                'format': tag.get('format').split(':')[-1] if tag.get('format') else None,
                'text': text if escape == False else None
            })

        self.data = lists

        return self

    def ix_non_fractions(self):
        """ iXBRLの非分数情報を取得する

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
        lists = []
        tags = self.soup.find_all(name='ix:nonFraction')
        for tag in tags:
            lists.append({
                'context_period': tag.get('contextRef').split("_")[0],
                'context_entity': tag.get('contextRef').split("_")[1] if len(tag.get('contextRef').split("_")) > 1 else None,
                'context_category': tag.get('contextRef').split("_")[2] if len(tag.get('contextRef').split("_")) > 2 else None,
                'decimals': int(tag.get('decimals')) if tag.get('decimals') else None,
                'format': tag.get('format'),
                'name': tag.get('name').replace(":", "_"),
                'scale': int(tag.get('scale')) if tag.get('scale') else None,
                'sign': tag.get('sign'),
                'unit_ref': tag.get('unitRef'),
                'xsi_nil': True if tag.get('xsi:nil') == 'true' else False,
                'numeric': float(re.sub(',','',tag.text)) if tag.text else None
            })

        self.data = lists

        return self