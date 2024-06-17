from PyXBRLTools.xbrl_manager.base_xbrl_manager import BaseXbrlManager
from PyXBRLTools.xbrl_parser.link_parser import CalLinkParser
import pandas

class LinkManager(BaseXbrlManager):
    def __init__(self, directory_path, role:str) -> None:
        super().__init__(directory_path)
        self.set_linkbase_files(role)
        self.label = None

    def set_link_roles(self, output_path, document_type = None):
        df = None
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if row["xlink_href"].endswith("lab.xml"):
                if df is None:
                    df = CalLinkParser.create(row["xlink_href"], output_path).link_roles().to_DataFrame()
                else:
                    df = pandas.concat([df, CalLinkParser.create(row["xlink_href"], output_path).link_roles().to_DataFrame()], ignore_index=True)

        self.label = df
        self.data = self.label

        return self