from xbrl_parser.ixbrl_parser import IxbrlParser
from xbrl_parser.label_parser import LabelParser

# テストコード
if __name__ == "__main__":
    file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Summary/tse-qcedjpsm-31210-20240613331210-ixbrl.htm"
    parser = IxbrlParser.create(file_path)
    print('ix_non_numeric**************************')
    print(parser.ix_non_numeric().to_DataFrame())
    print('ix_non_fractions**************************')
    print(parser.ix_non_fractions().to_DataFrame())
    print(parser.ix_non_fractions().to_dict())

    label_file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/tse-qcedjpfr-31210-2024-04-30-01-2024-06-13-lab.xml"
    label_parser = LabelParser.create(label_file_path)
    print(label_parser.link_labels().to_DataFrame())
    print(label_parser.link_locs().to_DataFrame())
    print(label_parser.link_label_arcs().to_DataFrame())