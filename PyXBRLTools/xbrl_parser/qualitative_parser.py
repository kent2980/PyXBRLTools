from bs4 import BeautifulSoup as bs
from pandas import DataFrame
import re
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import Utils

class QualitativeParser:
    """
    "qualitative.htm"から情報を解析して抽出するためのクラスです。
    """

    def __init__(self, file_path: str) -> None:
        """
        QualitativeParserクラスのコンストラクタです。
        """
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as file:
            self.soup = bs(file, features='html.parser')

    def get_smt_head(self) -> DataFrame:
        """
        HTMLファイルから見出しとテキストデータを抽出してDataFrameとして返すメソッドです。
        """
        lists = []
        head1_title = ""
        head2_title = ""

        for tag in self.soup.find_all(class_=True):
            class_ = tag["class"][0]

            if class_ == "smt_head1":
                head1_title = Utils.normalize_text(tag.text)
            elif class_ == "smt_head2":
                head2_title = Utils.normalize_text(tag.text)
            elif "smt_text" in class_:
                text = Utils.normalize_text(tag.text)
                if not lists or head1_title != lists[-1]['title'] or head2_title != lists[-1]['sub_title']:
                    lists.append({'title': head1_title, 'sub_title': head2_title, 'text': text})
                else:
                    lists[-1]['text'] += text

        lists = [row for row in lists if re.search(r'\d', row['title'])]
        return DataFrame(lists)

if __name__ == '__main__':
    file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/qualitative.htm"
    try:
        qp = QualitativeParser(file_path)
        df = qp.get_smt_head()

        os.makedirs("extract_csv/qualitative", exist_ok=True)
        df.to_csv('extract_csv/qualitative/qualitative.csv', index=False, encoding='utf-8-sig')
    except Exception as e:
        print(f"An error occurred: {e}")
