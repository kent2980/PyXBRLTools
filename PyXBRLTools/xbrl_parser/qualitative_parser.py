from PyXBRLTools.tests.xbrl_manager.test_base_xbrl_manager import test_xbrl_type
from .base_xbrl_parser import BaseXBRLParser
import re

class QualitativeParser(BaseXBRLParser):
    def smt_head(self):

        # h1とh2要素を取得して、辞書のリストとして抽出します
        titles = self.soup.find_all(['h1', 'h2'])
        content_list = []
        for title in titles:
            content_list.append({
                "title": title.text.strip(),
                "content": [p.text.strip().split(",") for p in title.find_next_siblings('p')]
            })

        self.data = content_list

        return self