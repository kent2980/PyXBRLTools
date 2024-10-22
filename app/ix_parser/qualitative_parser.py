import hashlib
import re
import time
import uuid
from pathlib import Path
from typing import Optional

import pandas
import requests

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

        # region プロパティの初期化

        type = None

        soup = self.soup

        lists = []

        is_main = False

        titleId, subTitleId, headingId = (
            None,
            None,
            None,
        )

        # endregion

        div_tags = soup.find_all("div")

        index = 0
        for div_tag in div_tags:

            # region タグの抽出

            target_class = [
                "p",
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "div",
                "table",
            ]

            text_tags = div_tag.find_all(
                name=target_class,
                recursive=False,
            )

            # endregion

            for i, tag in enumerate(text_tags):

                # テキストを整形処理
                text = scraping_text_transform(tag.get_text())

                # region 除外対象のタグをスキップ処理
                if tag.name in ["div", "table"]:
                    continue

                if i < len(text_tags) - 1:
                    if text_tags[i + 1].name in ["div", "table"]:
                        if tag.name == "p":
                            continue

                # textが空白の場合はスキップ
                if re.sub(r"\s", "", text) == "":
                    continue

                # textが1.で始まる場合は本文フラグをTrueにする
                if re.match(r"^1\.(?!.*…).*", text):
                    is_main = True

                if not is_main:
                    continue
                # endregion

                # xbrl_id,text,source_file_idから固有のIDを生成
                currentId = get_hash_id(
                    self.xbrl_id, text, self.source_file_id, index
                )

                # テキストのタイプとIDを設定
                parentId, titleId, subTitleId, headingId, type = (
                    classify_text_and_set_ids(
                        text, currentId, titleId, subTitleId, headingId
                    )
                )

                # 本文のテキストをlistsに追加
                if is_main:
                    lists.append(
                        QualitativeDocument(
                            currentId=currentId,
                            parentId=parentId,
                            content=text,
                            xbrl_id=self.xbrl_id,
                            source_file_id=self.source_file_id,
                            type=type,
                        )
                    )

                index += 1

        # orderを設定
        parentIdLst = []
        for item in lists:
            item: QualitativeDocument = item
            order = parentIdLst.count(item.parentId)
            item.order = order
            parentIdLst.append(item.parentId)

        self._set_data(lists)

        return self

    def set_photo_info(self):
        """画像情報を設定する"""

        if type(self.data) is not list:
            raise Exception("dataがリスト型ではありません。")

        parentId = None
        subtitleId = None

        for item in self.data:
            item: QualitativeDocument = item
            if item.content.startswith("1."):
                parentId = item.currentId
            if parentId == item.parentId:
                if item.content.startswith("(1)"):
                    subtitleId = item.currentId
            if subtitleId == item.parentId:
                if item.type == "heading":

                    if item.photo_url is not None:
                        continue

                    API_KEY = "29673097-4f37110575551aebc081c6b86"
                    query = item.content.replace("事業", "").replace(
                        "セグメント", ""
                    )
                    url = f"https://pixabay.com/api/?key={API_KEY}&q={query}&image_type=photo"

                    data = None

                    for _ in range(2):  # Try up to 2 times
                        response = requests.get(url)
                        if response.status_code == 200:
                            data = response.json()
                            break
                        else:
                            print(
                                f"Error {response.status_code}: Retrying in 60 seconds..."
                            )
                            time.sleep(60)

                    if data is None or data["total"] == 0:
                        print(f"Failed to get data from {url}")
                        item.photo_url = None
                    else:
                        url = data["hits"][0]["webformatURL"]
                        item.photo_url = url


def scraping_text_transform(text):
    """スクレイピングしたテキストを整形する関数"""

    # textの全角数字と全角かっこを半角数字と半角かっこに変換
    text = re.sub(
        r"[０-９（）．％［］＜＞]",
        lambda x: chr(ord(x.group(0)) - 0xFEE0),
        text,
    )

    # textの空白を削除
    text = re.sub(r" |　| ", "", text)

    # textの改行を削除
    text = re.sub(r"\n", "", text)

    return text


def get_hash_id(xbrl_id, text, source_file_id, index):
    """固有のIDを生成する関数"""

    hash_object = hashlib.md5(
        f"{xbrl_id}{text}{source_file_id}{str(index)}".encode()
    )
    return str(uuid.UUID(hash_object.hexdigest()))


def classify_text_and_set_ids(
    text, currentId, titleId, subTitleId, headingId
):
    """テキストタイプとIDを設定する関数"""

    if re.match(r"^[0-9]\.(?!.*…)", text):
        type = "title"
        titleId = currentId
        subTitleId, headingId, parentId = None, None, None
    elif re.match(r"^\([0-9]\)", text):
        type = "sub_title"
        subTitleId = currentId
        headingId = None
        parentId = titleId
    elif (
        re.match(
            r"^\【.*\】$|^\[.*\]$|^\(.*\)$|^[①-⑨].*|^\「.*\」$|^\<.*\>$|^.\..*",
            text,
        )
        and re.match(r"^(?!.*\(注.*\)).*", text)
        and not re.match(r"^(?=.*です.*)|^(?=.*ます.*)", text)
    ):
        type = "heading"
        headingId = currentId
        if subTitleId is None:
            parentId = titleId
        else:
            parentId = subTitleId
    elif re.match(r".*事業$", text):
        type = "heading"
        headingId = currentId
        if subTitleId is None:
            parentId = titleId
        else:
            parentId = subTitleId
    elif re.match(r".*セグメント$", text):
        type = "heading"
        headingId = currentId
        if subTitleId is None:
            parentId = titleId
        else:
            parentId = subTitleId
    else:
        type = "content"
        if headingId is None:
            parentId = subTitleId
            if subTitleId is None:
                parentId = titleId
        else:
            parentId = headingId

    return parentId, titleId, subTitleId, headingId, type


if __name__ == "__main__":
    parser = QualitativeParser(
        "/Users/user/Documents/tdnet/xbrl/20240809/XBRLData 4/Attachment/qualitative.htm"
    )
    parser.set_qualitative_info()
    parser.set_photo_info()
    lists = parser.data
    pandas.DataFrame(lists).to_csv("qualitative.csv", index=False)
