from xbrl_parser.ixbrl_parser import IxbrlParser
from xbrl_parser.xml_schema_parser import XmlSchemaParser
from xbrl_parser.xml_label_parser import XmlLabelParser

class XbrlParserController:

    def ixbrl_parser(file_path:str) -> IxbrlParser:
        """ iXBRLパーサを取得します。"""
        return IxbrlParser(file_path)

    def xml_schema_parser(file_path:str) -> XmlSchemaParser:
        """ XMLスキーマパーサを取得します。"""
        return XmlSchemaParser(file_path)

    def xml_label_parser(file_path:str = None) -> XmlLabelParser:
        """ XMLラベルパーサを取得します。"""
        return XmlLabelParser(file_path)

if __name__ == '__main__':
    ix = XbrlParserController().ixbrl_parser("")
    ix.ix_non_fractions