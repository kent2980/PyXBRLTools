from bs4 import BeautifulSoup as bs
from pandas import DataFrame

class XmlManifestparser:

    def __init__(self, file_path:str) -> None:
        self.__file_path = file_path
        self.__soup = bs(open(file_path), features='xml')

        s