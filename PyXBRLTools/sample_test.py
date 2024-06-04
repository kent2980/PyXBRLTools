from xbrl_manager.label_manager import LabelManager
from xbrl_parser.xbrl_ixbrl_parser import XbrlIxbrlParser
import pandas as pd
from db_connector.postgre_sql_connector import PostgreSqlConnector

if __name__ == "__main__":
    print("LabelManager test")

    xbrl_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Summary/tse-acedjpsm-57210-20240507583360-ixbrl.htm"
    xbrl_parser = XbrlIxbrlParser(xbrl_path)
    non_fractions = xbrl_parser.ix_non_numerics
    name_list = non_fractions['name'].tolist()

    extra_dir = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir"
    lm = LabelManager(extra_dir)

    connector = PostgreSqlConnector("localhost", 5432, "fsstock", "postgres", "full6839")
    connector.connect()
    connector.create_table_from_df("non_fractions", non_fractions)
    connector.create_table_from_df("label_table", lm.labels_table_df(name_list))
    connector.create_table_from_df("locs_table", lm.locs_table_df(name_list))
    connector.create_table_from_df("arcs_table", lm.arcs_table_df(name_list))
    connector.create_table_from_df("role_refs_table", lm.role_refs_table_df(name_list))
    connector.disconnect()