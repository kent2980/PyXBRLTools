import re
import uuid
from typing import Optional

from app.ix_parser import BaseXBRLParser
from app.ix_tag import QualitativeDocument


class QualitativeParser(BaseXBRLParser):
    """XBRLドキュメントから定性データを解析するためのクラス"""

    def __init__(
        self, xbrl_url, output_path=None, xbrl_id: Optional[str] = None
    ):
        super().__init__(xbrl_url, output_path, xbrl_id)
        # ファイル名を検証
        self._assert_valid_basename("qualitative.htm")

    def set_qualitative_info(self):
        lists = []  # 定性的情報を格納するリスト
        tags = self.soup.find_all(True)  # タグを取得
        order = 0
        content, titleId, parentId = (
            None,
            None,
            None,
        )
        i = 0
        is_add, is_read, is_first_head = False, False, False
        # データ取得
        for tag in tags:
            documentId = str(uuid.uuid4())

            if tag.get("class") is None:  # クラス属性がない場合はスキップ
                continue
            if (
                "head" in tag.get("class") and not is_first_head
            ):  # headタグが最初に出現するまでスキップ
                is_first_head = True
                continue
            if (
                len(re.sub(r"\s+", "", tag.get_text())) == 0
            ):  # テキストが空白の場合はスキップ
                continue
            if "head" not in tag.get("class") and "text" not in tag.get(
                "class"
            ):  # headタグとtextタグ以外はスキップ
                continue
            if "head" in tag.get(
                "class"
            ):  # headタグが出現したらis_readをTrueにする
                is_read = True
            if is_read == False:  # is_readがFalseの場合はスキップ
                continue

            if "head" in tag.get("class"):  # headタグの場合
                content = re.sub(r"\s+", "", tag.get_text())
                is_add = True

            if "head2" in tag.get("class"):
                if not re.match(r"[\(\（](.*?)[\)\）]", content):
                    parentId = None
                    titleId = documentId
                    type = "title"
                else:
                    parentId = titleId
                    type = "subtitle"

            elif "text" in tag.get("class"):
                type = "content"
                content = re.sub(r"\s+", "", tag.get_text())
                is_add = True
                if parentId is None:
                    is_add = False
            else:
                is_add = False

            if is_add:
                lists.append(
                    QualitativeDocument(
                        currentId=documentId,
                        xbrl_id=self.xbrl_id,
                        content=content,
                        order=order,
                        parentId=parentId,
                        type=type,
                        source_file_id=self.source_file_id,
                    )
                )
                is_add = False

                if "head" in tag.get("class"):
                    parentId = documentId
                    order = 0
                else:
                    order += 1

            i += 1

        lists2 = []
        content = None
        # データ結合
        for i, item in enumerate(lists):
            if isinstance(item, QualitativeDocument):
                if "title" in item.type:
                    content = item.content.translate(
                        str.maketrans(
                            "０１２３４５６７８９（）．", "0123456789()."
                        )
                    )
                    lists2.append(
                        QualitativeDocument(
                            currentId=item.currentId,
                            xbrl_id=item.xbrl_id,
                            content=content.replace('"', ""),
                            order=item.order,
                            parentId=item.parentId,
                            type=item.type,
                            source_file_id=item.source_file_id,
                        )
                    )
                    content = None
                elif "subtitle" in item.type:
                    content = item.content.translate(
                        str.maketrans(
                            "０１２３４５６７８９（）．", "0123456789()."
                        )
                    )
                    lists2.append(
                        QualitativeDocument(
                            currentId=item.currentId,
                            xbrl_id=item.xbrl_id,
                            content=content.replace('"', ""),
                            order=item.order,
                            parentId=item.parentId,
                            type=item.type,
                            source_file_id=item.source_file_id,
                        )
                    )
                elif "content" in item.type:
                    try:
                        if "title" in lists[i + 1].type:
                            if content is not None:
                                content = content + item.content
                            else:
                                content = item.content
                            content = content.translate(
                                str.maketrans(
                                    "０１２３４５６７８９（）．",
                                    "0123456789().",
                                )
                            )
                            lists2.append(
                                QualitativeDocument(
                                    currentId=item.currentId,
                                    xbrl_id=item.xbrl_id,
                                    content=content.replace('"', ""),
                                    order=item.order,
                                    parentId=item.parentId,
                                    type=item.type,
                                    source_file_id=item.source_file_id,
                                )
                            )
                            content = None
                        elif "title" in lists[i - 1].type:
                            content = item.content
                        elif "content" in lists[i - 1].type:
                            content = content + item.content
                    except IndexError:
                        lists2.append(
                            QualitativeDocument(
                                currentId=item.currentId,
                                xbrl_id=item.xbrl_id,
                                content=content.replace('"', ""),
                                order=item.order,
                                parentId=item.parentId,
                                type=item.type,
                                source_file_id=item.source_file_id,
                            )
                        )

        parentIds = []
        for item in lists2:
            order = parentIds.count(item.parentId)
            item.order = order
            parentIds.append(item.parentId)

        self._set_data(lists2)

        return self


if __name__ == "__main__":
    parser = QualitativeParser(
        "/Users/user/Documents/tdnet/xbrl/20240809/XBRLData 3/Attachment/qualitative.htm"
    )
    parser.set_qualitative_info()
    print(parser.data)
    # dataをテキストファイルに出力
    parser.to_DataFrame().to_csv("qualitative.csv", index=False)
