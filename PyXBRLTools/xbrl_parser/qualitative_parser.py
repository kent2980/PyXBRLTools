from PyXBRLTools.xbrl_exception.xbrl_parser_exception import TypeOfXBRLIsDifferent
from .base_xbrl_parser import BaseXBRLParser

class QualitativeParser(BaseXBRLParser):
    """
    XBRLドキュメントから定性データを解析するためのクラスです。

    このクラスはBaseXBRLParserクラスを拡張し、XBRLドキュメントから定性データを解析するためのメソッドを提供します。
    ドキュメントのHTMLコンテンツから特定のタグを抽出し、それらを構造化された形式で整理します。

    Args:
        xbrl_url (str): XBRLドキュメントのURLです。
        output_path (str): 解析結果を保存するファイルのパスです。

    Properties:
        data (list): 解析された定性データを含む辞書のリストです。

    Methods:
        smt_head: ドキュメントのHTMLコンテンツから特定のタグを抽出し、それらを構造化された形式で整理します。

    Raises:
        ValueError: ドキュメントが定性データでない場合に発生します。

    Examples:
        >>> parser = QualitativeParser.create("https://www.example.com/xbrl/qualitative.htm")
        >>> parser.smt_head()
        >>> print(parser.data)
    """

    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path)
        if self.basename() != "qualitative.htm":
            raise TypeOfXBRLIsDifferent(f"{self.basename()} はqualitative.htmではありません。")

    def qualitative_info(self):
        lists = []
        tags = self.soup.find_all(True)
        head2, head3, head4, content = "", "", "", ""
        class_names = ['smt_head2', 'smt_head3', 'smt_text3']

        for tag in tags:
            if len(tag.get_text(strip=True)) == 0:
                continue

            tag_class = tag.get("class")
            text = tag.get_text(strip=True)

            if tag_class in class_names:
                if head2 != text or head3 != text:
                    if head2 != "":
                        lists.append({"head2": head2, "head3": head3, "head4":head4, "content": content})
                    content = ""
                if tag_class == 'smt_head2':
                    head2 = text
                    head4 = ""
                elif tag_class == 'smt_head3':
                    head3 = text
                elif tag_class == 'smt_text3':
                    head4 = text
            else:
                content += text

        self.data = lists

        return self