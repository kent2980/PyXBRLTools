from bs4 import BeautifulSoup as bs
from pandas import DataFrame

class Xsds:

    def __init__(self, xsd_path:str) -> None:
        self.__xsd_path = xsd_path
        self.soup = bs(open(self.__xsd_path), features='xml') if xsd_path else None

        self.__import_schema:DataFrame = None
        self.__link_base_refs:DataFrame = None
        self.__elements:DataFrame = None

    def init_df(self):
        if self.__xsd_path is not None:
            self.__import_schema:DataFrame = self.import_schema()
            self.__link_base_refs:DataFrame = self.link_base_refs()
            self.__elements:DataFrame = self.elements()


    def import_schema(self):
        pass

    def link_base_refs(self):
        pass

    def elements(self):
        pass