from .base_xbrl_parser import BaseXBRLParser
import re
from pandas import DataFrame

class QualitativeParser(BaseXBRLParser):
    def smt_head(self):

        # h1とh2,p2要素を取得して、辞書のリストとして抽出します
        tags = self.soup.find_all(['h1', 'h2', 'h3', 'p'])
        content_list = []
        tag, tag_id, tag_class, tag_text = None, None, None, None
        for tag in tags:
          if len(tag.get_text(strip=True)) == 0:
            continue
          content_list.append({
            'tag': tag.name,
            'id':  tag.get('id'),
            'class': tag.get('class'),
            'text': tag.get_text(strip=True).replace(" ", "").replace("　", "")
          })

        df = DataFrame(content_list)
        # head1,head2,head3,hea4が同じである場合、グループ化してtextを連結します
        # df = df.groupby(['tag', 'class'])['text'].apply(' '.join).reset_index()
        # dfの全ての要素の全角文字を半角文字に変換します
        df = df.applymap(lambda x: x.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
                        if isinstance(x, str) else x)
        self.data = df.to_dict(orient='records')

        return self