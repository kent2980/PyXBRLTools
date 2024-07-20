from app.exception import TagNotFoundError, TypeOfXBRLIsDifferent
from app.tag import (
    LabelArc,
    LabelLoc,
    LabelRoleRefs,
    LabelValue,
    SourceFile,
)

from . import BaseXBRLParser


class LabelParser(BaseXBRLParser):
    """XBRLのラベル情報を取得するクラス"""

    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path)

        # ファイル名がlab.xmlでない場合はエラーを発生
        if not self.basename.endswith(("lab.xml", "lab-en.xml")):
            raise TypeOfXBRLIsDifferent(
                f"{self.basename} はlab.xmlではありません。"
            )

        # 初期化メソッド
        self._set_source_file(self.basename, "labelLinkbaseRef")

    def link_labels(self):
        """link:label要素を取得するメソッド。

        returns:
            self: LabelParser
        """

        lists = []

        tags = self.soup.find_all(name=["link:label", "label"])
        for tag in tags:

            xlink_label = tag.get("xlink:label")

            # ファイル名にtseが含まれている場合
            if "tse" in self.basename:
                # xlink_labelにtseが含まれていない場合はスキップ
                if "tse" not in xlink_label:
                    continue

            lv = LabelValue(
                xlink_type=tag.get("xlink:type"),
                xlink_label=xlink_label,
                xlink_role=tag.get("xlink:role"),
                xml_lang=tag.get("xml:lang"),
                label=tag.text,
                source_file_id=self.source_file.id,
            )
            lists.append(lv.__dict__)

        self._set_data(lists)

        return self

    def link_label_locs(self):
        """link:loc要素を取得するメソッド。

        returns:
            self: LabelParser
        """
        lists = []

        tags = self.soup.find_all(name=["link:loc", "loc"])
        for tag in tags:

            # _____attr[xlink:href]
            if tag.get("xlink:href"):
                xlink_schema = (
                    tag.get("xlink:href").split("#")[0].split("/")[-1]
                )
                xlink_href = tag.get("xlink:href").split("#")[-1:][0]

                # ファイル名にtseが含まれている場合
                if "tse" in self.basename:
                    # xlink_hrefにtseが含まれていない場合はスキップ
                    if "tse" not in xlink_href:
                        continue

            else:
                xlink_schema = None
                xlink_href = None

            ll = LabelLoc(
                xlink_type=tag.get("xlink:type"),
                xlink_label=tag.get("xlink:label"),
                xlink_schema=xlink_schema,
                xlink_href=xlink_href,
                source_file_id=self.source_file.id,
            )
            lists.append(ll.__dict__)

        self._set_data(lists)

        return self

    def link_label_arcs(self):
        """link:labelArc要素を取得するメソッド。

        returns:
            self: LabelParser
        """
        lists = []
        tags = self.soup.find_all(name=["link:labelArc", "labelArc"])
        for tag in tags:

            xlink_from = tag.get("xlink:from")
            xlink_to = tag.get("xlink:to")

            # ファイル名にtseが含まれている場合
            if "tse" in self.basename:
                # xlink_from, xlink_toにtseが含まれていない場合はスキップ
                if "tse" not in xlink_from or "tse" not in xlink_to:
                    continue

            la = LabelArc(
                xlink_type=tag.get("xlink:type"),
                xlink_arcrole=tag.get("xlink:arcrole"),
                xlink_from=tag.get("xlink:from"),
                xlink_to=tag.get("xlink:to"),
                source_file_id=self.source_file.id,
            )
            lists.append(la.__dict__)

        self._set_data(lists)

        return self

    def role_refs(self):
        """roleRef要素を取得するメソッド。

        returns:
            self: LabelParser

        Raises:
            TagNotFoundError: roleRef要素が存在しない場合に発生します。
        """
        lists = []
        tags = self.soup.find_all(name=["link:roleRef", "roleRef"])

        if len(tags) == 0:
            raise TagNotFoundError("roleRef要素が存在しません。")

        for tag in tags:
            # _____attr[xlink:href]
            if tag.get("xlink:href"):
                xlink_schema = tag.get("xlink:href").split("#")[0]
                xlink_href = tag.get("xlink:href").split("#")[-1:][0]

                # ファイル名にtseが含まれている場合
                if "tse" in self.basename:
                    # xlink_schemaにtseが含まれていない場合はスキップ
                    if "tse" not in xlink_schema:
                        continue

            else:
                xlink_schema = None
                xlink_href = None

            lrr = LabelRoleRefs(
                role_uri=tag.get("roleURI"),
                xlink_type=tag.get("xlink:type"),
                xlink_schema=xlink_schema,
                xlink_href=xlink_href,
            )

            lists.append(lrr.__dict__)

        self._set_data(lists)

        return self
