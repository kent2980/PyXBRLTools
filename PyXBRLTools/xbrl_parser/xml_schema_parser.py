from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from abc import ABC, abstractmethod

class BaseXmlSchemaParser(ABC):

    def __init__(self, file_path:str) -> None:
        self.__file_path = file_path
        self.soup = bs(open(self.__file_path), features='xml')

        self.__import_schemas:DataFrame = None
        self.__link_base_refs:DataFrame = None
        self.__elements:DataFrame = None

        self.__set_df()

    def __set_df(self):
        if self.__file_path is not None:
            self.__import_schemas:DataFrame = self.get_import_schemas()
            self.__link_base_refs:DataFrame = self.get_link_base_refs()
            self.__elements:DataFrame = self.get_elements()

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path:str):
        self.__file_path = file_path
        self.soup = bs(open(file_path), features='xml')
        self.__set_df()

    @property
    def import_schemas(self):
        return self.__import_schemas

    @property
    def link_base_refs(self):
        return self.__link_base_refs

    @property
    def elements(self):
        return self.__elements

    @abstractmethod
    def get_import_schemas(self):
        pass

    @abstractmethod
    def get_link_base_refs(self):
        pass

    @abstractmethod
    def get_elements(self):
        pass

class XmlSchemaParser(BaseXmlSchemaParser):

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

    def get_import_schemas(self):
        lists = []

        tags = self.soup.find_all(name='import')
        for tag in tags:
            dict = {
                'schema_location': tag.get('schemaLocation'),
                'name_space': tag.get('namespace')
            }

            lists.append(dict)

        return DataFrame(lists)

    def get_link_base_refs(self):
        lists = []

        tags = self.soup.find_all(name='link:linkbaseRef')
        for tag in tags:
            dict = {
                'xlink_type': tag.get('xlink:type'),
                'xlink_href': tag.get('xlink:href'),
                'xlink_role': tag.get('xlink:role'),
                'xlink_arcrole': tag.get('xlink:arcrole')
            }

            lists.append(dict)

        return DataFrame(lists)

    def get_elements(self):
        lists = []

        tags = self.soup.find_all(name='element')
        for tag in tags:
            dict = {
                'id': tag.get('id'),
                'xbrli_balance': tag.get('xbrli:balance'),
                'xbrli_period_type': tag.get('xbrli:periodType'),
                'name': tag.get('name'),
                'nillable': tag.get('nillable'),
                'substitution_group': tag.get('substitutionGroup'),
                'type': tag.get('type')
            }
            lists.append(dict)

        return DataFrame(lists)

if __name__ == '__main__':
    file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-44440-2024-03-31-01-2024-05-14.xsd"
    xsds = XmlSchemaParser(file_path)
    print(xsds.elements)