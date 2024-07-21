from typing import Optional

from . import BaseXBRLParser


class QualitativeParser(BaseXBRLParser):
    """XBRLドキュメントから定性データを解析するためのクラス"""

    def __init__(
        self, xbrl_url, output_path=None, xbrl_id: Optional[str] = None
    ):
        super().__init__(xbrl_url, output_path, xbrl_id)

        # ファイル名を検証
        self._assert_valid_basename("qualitative.htm")

    def qualitative_info(self):
        lists = []
        tags = self.soup.find_all(True)
        head2, head3, head4, content = "", "", "", ""
        class_names = ["smt_head2", "smt_head3", "smt_text3"]

        for tag in tags:
            if len(tag.get_text(strip=True)) == 0:
                continue

            tag_class = tag.get("class")
            text = tag.get_text(strip=True)

            if tag_class in class_names:
                if head2 != text or head3 != text:
                    if head2 != "":
                        lists.append(
                            {
                                "head2": head2,
                                "head3": head3,
                                "head4": head4,
                                "content": content,
                            }
                        )
                    content = ""
                if tag_class == "smt_head2":
                    head2 = text
                    head4 = ""
                elif tag_class == "smt_head3":
                    head3 = text
                elif tag_class == "smt_text3":
                    head4 = text
            else:
                content += text

        self._set_data(lists)

        return self
