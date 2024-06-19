from .base_xbrl_parser import BaseXBRLParser
import re
from pandas import DataFrame

class QualitativeParser(BaseXBRLParser):
    def smt_head(self):
        lists = []
        # h1とh2,p2要素を取得して、辞書のリストとして抽出します
        tags = self.soup.find_all(True)
        title, content =  "", ""
        for tag in tags:
            tag_class = tag.get("class")
            class_names = ['smt_head1', 'smt_head2', 'smt_head3']
            if tag_class in class_names:
                if title != tag_class:
                    if title != "":
                        lists.append({"title": title, "content": content})
                    title = tag.get_text(strip=True)
                    content = ""
            else:
                content += tag.get_text(strip=True)


        self.data = lists

        return self