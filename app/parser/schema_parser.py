from app.exception import TypeOfXBRLIsDifferent
from app.tag import SchemaElement, SchemaImport, SchemaLinkBaseRef

from . import BaseXBRLParser


class SchemaParser(BaseXBRLParser):
    """ スキーマファイルを解析するクラス """

    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path)

        # ファイル名を検証
        self._assert_valid_basename(".xsd")

    def import_schemas(self):
        lists = []

        tags = self.soup.find_all(name="import")
        for tag in tags:

            si = SchemaImport(
                schema_location=tag.get("schemaLocation"),
                name_space=tag.get("namespace"),
                document_type=self.document_type,
            )

            lists.append(si)

        self._set_data(lists)

        return self

    def link_base_refs(self):
        lists = []

        tags = self.soup.find_all(name="linkbaseRef")
        for tag in tags:

            slb = SchemaLinkBaseRef(
                xlink_type=tag.get("xlink:type"),
                xlink_href=tag.get("xlink:href"),
                xlink_role=tag.get("xlink:role"),
                xlink_arcrole=tag.get("xlink:arcrole"),
                document_type=self.document_type,
            )

            lists.append(slb)

        self._set_data(lists)

        return self

    def elements(self):
        lists = []

        tags = self.soup.find_all(name="element")
        for tag in tags:

            se = SchemaElement(
                id=tag.get("id"),
                xbrli_balance=tag.get("xbrli:balance"),
                xbrli_period_type=tag.get("xbrli:periodType"),
                name=tag.get("name"),
                nillable=tag.get("nillable"),
                substitution_group=tag.get("substitutionGroup"),
                type=tag.get("type"),
                abstract=tag.get("abstract"),
                document_type=self.document_type,
            )

            lists.append(se)

        self._set_data(lists)

        return self
