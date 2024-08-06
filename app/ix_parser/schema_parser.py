from pathlib import Path
from typing import Optional

from app.ix_tag import SchemaElement, SchemaImport, SchemaLinkBaseRef
from app.utils import Utils

from . import BaseXBRLParser


class SchemaParser(BaseXBRLParser):
    """スキーマファイルを解析するクラス"""

    def __init__(
        self, xbrl_url, output_path=None, xbrl_id: Optional[str] = None
    ):
        super().__init__(xbrl_url, output_path, xbrl_id)

        # ファイル名を検証
        self._assert_valid_basename(".xsd")

    def import_schemas(self):
        lists = []

        tags = self.soup.find_all(name="import")
        for tag in tags:

            si = SchemaImport(
                schema_location=tag.get("schemaLocation"),
                name_space=tag.get("namespace"),
                xbrl_type=self.xbrl_type,
                xbrl_id=self.xbrl_id,
                source_file_id=self.source_file_id,
            )

            lists.append(si)

        self._set_data(lists)

        return self

    def link_base_refs(self, exclude: list = []):
        lists = []

        # 除外リスト

        tags = self.soup.find_all(name="linkbaseRef")
        for tag in tags:

            xlink_href = tag.get("xlink:href")
            if xlink_href:
                if xlink_href.startswith("http"):
                    source_file_id = str(Utils.string_to_uuid(xlink_href))
                else:
                    source_file_id = str(
                        Utils.string_to_uuid(
                            f"{self.xbrl_id}{Path(xlink_href).name}"
                        )
                    )

                # excludeリストの要素文字列がxlink_hrefに含まれている場合はスキップ
                if any([e in xlink_href for e in exclude]):
                    continue

            slb = SchemaLinkBaseRef(
                xlink_type=tag.get("xlink:type"),
                xlink_href=tag.get("xlink:href"),
                xlink_role=tag.get("xlink:role"),
                xlink_arcrole=tag.get("xlink:arcrole"),
                xbrl_type=self.xbrl_type,
                xbrl_id=self.xbrl_id,
                source_file_id=self.source_file_id,
                href_source_file_id=source_file_id,
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
                xbrl_type=self.xbrl_type,
                xbrl_id=self.xbrl_id,
                source_file_id=self.source_file_id,
            )

            lists.append(se)

        self._set_data(lists)

        return self
