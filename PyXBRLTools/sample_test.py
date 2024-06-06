from xbrl_parser.xml_link_parser import XmlLinkParser

if __name__ == "__main__":
    print("Test sample")

    file_path = "doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-57210-2024-03-31-01-2024-05-13-def.xml"
    xbrl_parser = XmlLinkParser(file_path)
    print(xbrl_parser.link)
    print(xbrl_parser.link_arcs)
    print(xbrl_parser.link_roles)
    print(xbrl_parser.link_base)
    print(xbrl_parser.link_locs)
    role_uri = "http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedStatementOfChangesInEquity"

    print(f'selected_link_arcs 読み込み中・・・:[{role_uri}]')
    print(xbrl_parser.get_selected_link_arcs(role_uri))
    print(f'selected_link_locs 読み込み中・・・:[{role_uri}]')
    print(xbrl_parser.get_selected_link_locs(role_uri))
    print(f'role_uriが存在するか確認中・・・:[{role_uri}]')
    print(xbrl_parser.is_role_exist(role_uri))
