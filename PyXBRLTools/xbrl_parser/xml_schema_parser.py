from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from abc import ABC, abstractmethod
import os
import logging
from log.py_xbrl_tools_loging import PyXBRLToolsLogging

class BaseXmlSchemaParser(ABC):
    """ XMLスキーマパーサの基底クラスです。
    XMLスキーマの情報を取得するクラスです。
    """

    def __init__(self, file_path:str) -> None:
        """ BaseXmlSchemaParserのコンストラクタです。

        Args:
            file_path (str): XMLファイルのパス。
        """
        self.__file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as file:
            self.soup = bs(file, features='lxml-xml')

        # ログ設定
        class_name = self.__class__.__name__
        self.logger = PyXBRLToolsLogging(log_level=logging.DEBUG)
        self.logger.set_log_file(f'Log/{class_name}.log')

    @property
    def file_path(self) -> str:
        """ ファイルパスを取得します。

        returns:
            str: ファイルパス。
        """
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path:str):
        """ ファイルパスを設定します。

        Args:
            file_path (str): ファイルパス。
        """
        self.__file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as file:
            self.soup = bs(file, features='lxml-xml')

    @abstractmethod
    def get_import_schemas(self) -> DataFrame:
        """ importスキーマを取得します。"""
        pass

    @abstractmethod
    def get_link_base_refs(self) -> DataFrame:
        """ link_base_refsを取得します。"""
        pass

    @abstractmethod
    def get_elements(self) -> DataFrame:
        """ elementsを取得します。"""
        pass

class XmlSchemaParser(BaseXmlSchemaParser):
    """
    XMLスキーマパーサの具象クラスです。
    XMLスキーマの情報を取得するクラスです。
    """

    def get_import_schemas(self) -> DataFrame:
        """ importスキーマを取得します。

        returns:
            DataFrame: importスキーマテーブルのDataFrame。

        example:
        get_import_schemas()の出力例
        >>> df = get_import_schemas()
            print(df)
        output:
        |    | schema_location | name_space |
        |----|-----------------|------------|
        | 0  | http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd | http://www.xbrl.org/2003/instance |
        | 1  | http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd | http://www.xbrl.org/2003/instance |
        | 2  | http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd | http://www.xbrl.org/2003/instance |
        """
        lists = []

        tags = self.soup.find_all(name='import')
        for tag in tags:
            dict = {
                'schema_location': tag.get('schemaLocation'),
                'name_space': tag.get('namespace')
            }

            lists.append(dict)

        return DataFrame(lists)

    def get_link_base_refs(self) -> DataFrame:
        """ link_base_refsを取得します。

        returns:
            DataFrame: link_base_refsテーブルのDataFrame。

        example:
        get_link_base_refs()の出力例
        >>> df = get_link_base_refs()
            print(df)
        output:
        |    | xlink_type | xlink_href | xlink_role | xlink_arcrole |
        |----|------------|------------|------------|---------------|
        | 0  | simple | http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd | http://www.xbrl.org/2003/role/linkbaseRef | None |
        | 1  | simple | http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd | http://www.xbrl.org/2003/role/linkbaseRef | None |
        | 2  | simple | http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd | http://www.xbrl.org/2003/role/linkbaseRef | None |
        """
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

    def get_elements(self) -> DataFrame:
        """ elementsを取得します。

        returns:
            DataFrame: elementsテーブルのDataFrame。

        example:
        get_elements()の出力例
        >>> df = get_elements()
            print(df)
        output:
        |    | id | xbrli_balance | xbrli_period_type | name | nillable | substitution_group | type |
        |----|----|---------------|-------------------|------|----------|--------------------|------|
        | 0  | jpcrp_cor:DocumentType | credit | duration | ドキュメントタイプ | false | xbrli:item | xbrli:stringItemType |
        | 1  | jpcrp_cor:DocumentType | debit | duration | ドキュメントタイプ | false | xbrli:item | xbrli:stringItemType |
        | 2  | jpcrp_cor:DocumentType | credit | duration | ドキュメントタイプ | false | xbrli:item | xbrli:stringItemType |
        """
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
    file_path = "doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-57210-2024-03-31-01-2024-05-13.xsd"
    output_dir = "extract_csv/schema"
    xsds = XmlSchemaParser(file_path)

    os.makedirs(output_dir,exist_ok=True)
    xsds.get_link_base_refs.to_csv(f"{output_dir}/linkBaseRef.csv",encoding='utf-8-sig')
    xsds.get_import_schemas.to_csv(f"{output_dir}/importSchema.csv",encoding='utf-8-sig')
    xsds.get_elements.to_csv(f"{output_dir}/element.csv",encoding='utf-8-sig')