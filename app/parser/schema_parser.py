from app.exception import TypeOfXBRLIsDifferent

from . import BaseXBRLParser


class SchemaParser(BaseXBRLParser):
    """スキーマファイルを解析するクラス

    Attributes:
        soup (BeautifulSoup): BeautifulSoupオブジェクト
        data (list): 解析結果を格納するリスト

    Properties:
        import_schemas: importタグの情報を取得する
        link_base_refs: linkbaseRefタグの情報を取得する
        elements: elementタグの情報を取得する

    Examples:
        >>> from PyXBRLTools.xbrl_manager.schema_manager import SchemaManager
        >>> schema_manager = SchemaManager.create("path/to/schema_file.xsd")
        >>> schema_manager.parser.import_schemas()
        >>> schema_manager.parser.link_base_refs()
        >>> schema_manager.parser.elements()
    """

    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path)

        # xsd.xml以外のファイルはエラーを出力する
        if not self.basename().endswith(".xsd"):
            raise TypeOfXBRLIsDifferent(f"{self.basename()} は[.xsd]ではありません。")

    def import_schemas(self):
        lists = []

        tags = self.soup.find_all(name="import")
        for tag in tags:
            dict = {
                "schema_location": tag.get("schemaLocation"),
                "name_space": tag.get("namespace"),
                "document_type": self.document_type,
            }

            lists.append(dict)

        self.data = lists

        return self

    def link_base_refs(self):
        lists = []

        tags = self.soup.find_all(name="linkbaseRef")
        for tag in tags:
            dict = {
                "xlink_type": tag.get("xlink:type"),
                "xlink_href": tag.get("xlink:href"),
                "xlink_role": tag.get("xlink:role"),
                "xlink_arcrole": tag.get("xlink:arcrole"),
                "document_type": self.document_type,
            }

            lists.append(dict)

        self.data = lists

        return self

    def elements(self):
        lists = []

        tags = self.soup.find_all(name="element")
        for tag in tags:
            dict = {
                "id": tag.get("id"),
                "xbrli_balance": tag.get("xbrli:balance"),
                "xbrli_period_type": tag.get("xbrli:periodType"),
                "name": tag.get("name"),
                "nillable": tag.get("nillable"),
                "substitution_group": tag.get("substitutionGroup"),
                "type": tag.get("type"),
                "abstract": tag.get("abstract"),
                "document_type": self.document_type,
            }

            lists.append(dict)

        self.data = lists

        return self
