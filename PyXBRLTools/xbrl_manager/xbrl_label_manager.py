from xbrl_parser.xml_label_parser import XmlLabelParser
from xbrl_manager.xbrl_path_manager import XbrlPathManager

class BaseXbrlLabelManager(XbrlPathManager):
    def __init__(self, xbrl_directory_path :str):

        if xbrl_directory_path is None:
            raise ValueError('XBRLファイルのディレクトリパスが指定されていません。')

        super().__init__(xbrl_directory_path)
        self.__label_path = self.label_path
        self.__label_parser = XmlLabelParser()

    @property
    def label_path(self):
        return self.__label_path

    @property
    def label_parser(self):
        return self.__label_parser

class XbrlLabelManager(BaseXbrlLabelManager):
    pass
