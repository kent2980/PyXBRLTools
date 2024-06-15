from .base_xbrl_parser import BaseXBRLParser
import re

class QualitativeParser(BaseXBRLParser):
    def smt_head(self):

        lists = []
        head1_title = ""
        head2_title = ""

        for tag in self.soup.find_all(class_=True):
            class_ = tag["class"][0]

            if class_ == "smt_head1":
                head1_title = tag.text
            elif class_ == "smt_head2":
                head2_title = tag.text
            elif "smt_text" in class_:
                text = tag.text
                if not lists or head1_title != lists[-1]['title'] or head2_title != lists[-1]['sub_title']:
                    lists.append({'title': head1_title, 'sub_title': head2_title, 'text': text})
                else:
                    lists[-1]['text'] += text

        lists = [row for row in lists if re.search(r'\d', row['title'])]

        self.data = lists

        return self