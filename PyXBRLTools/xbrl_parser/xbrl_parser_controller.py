from xbrl_parser.ixbrl_parser import IxbrlParser
from xbrl_parser.xml_schema_parser import XmlSchemaParser
from xbrl_parser.xml_label_parser import XmlLabelParser

class XbrlParserController:

    def ixbrl_parser(file_path:str) -> IxbrlParser:
        return IxbrlParser(file_path)

    def xml_schema_parser(file_path:str) -> XmlSchemaParser:
        return XmlSchemaParser(file_path)

    def xml_label_parser(file_path:str) -> XmlLabelParser:
        return XmlLabelParser(file_path)

if __name__ == '__main__':
    ix = XbrlParserController().ixbrl_parser("")
    ix.ix_non_fractions