from PyXBRLTools.tests.xbrl_manager.test_base_xbrl_manager import test_xbrl_type
from .base_xbrl_parser import BaseXBRLParser
import re

class QualitativeParser(BaseXBRLParser):
    def smt_head(self):

        # h1とh2,p2要素を取得して、辞書のリストとして抽出します
        tags = self.soup.find_all(['h1', 'h2', 'p'])
        content_list = []
        for tag in tags:
            content_list.append({
              'tag': tag.name,
              'text': tag.get_text(strip=True)
            })

        self.data = content_list

        return self