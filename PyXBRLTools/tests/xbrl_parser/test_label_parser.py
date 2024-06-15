import pytest
from bs4 import BeautifulSoup as bs
from PyXBRLTools.xbrl_parser.label_parser import LabelParser
import os

@pytest.fixture
def label_parser():
    xbrl_url = "http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2022-11-01/jpcrp_cor_2022-11-01.xsd"
    output_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/TEST"
    return LabelParser(xbrl_url, output_path)

def test_link_labels(label_parser):
    # ダミーのXMLを作成
    xml_content = """
<link:linkbase xmlns:link="http://www.xbrl.org/2003/linkbase" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xbrli="http://www.xbrl.org/2003/instance">
  <link:roleRef roleURI="http://disclosure.edinet-fsa.go.jp/jpcrp/std/alt/role/label" xlink:type="simple" xlink:href="../../../jpcrp/2022-11-01/jpcrp_rt_2022-11-01.xsd#rol_std_altLabel"/>
    <link:labelLink xlink:type="extended" xlink:role="http://www.xbrl.org/2003/role/link">
    <link:loc xlink:type="locator" xlink:href="../jppfs_cor_2022-11-01.xsd#jppfs_cor_AssetsAbstract" xlink:label="AssetsAbstract"/>
    <link:label xlink:type="resource" xlink:label="label_AssetsAbstract" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="ja" id="label_AssetsAbstract">資産の部</link:label>
    <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label" xlink:from="AssetsAbstract" xlink:to="label_AssetsAbstract"/>
    <link:loc xlink:type="locator" xlink:href="../jppfs_cor_2022-11-01.xsd#jppfs_cor_CurrentAssetsAbstract" xlink:label="CurrentAssetsAbstract"/>
    <link:label xlink:type="resource" xlink:label="label_CurrentAssetsAbstract" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="ja" id="label_CurrentAssetsAbstract">流動資産</link:label>
    <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label" xlink:from="CurrentAssetsAbstract" xlink:to="label_CurrentAssetsAbstract"/>
  </link:labelLink>
</link:linkbase>
    """
    # Set the BeautifulSoup object of the label_parser
    label_parser.soup = bs(xml_content, "xml")
    # Call the link_labels method
    result = label_parser.link_labels()
    # Check if the result is a LabelParser object
    assert isinstance(result, LabelParser)
    # Check if the data attribute is populated with the expected values
    result_dict = result.to_dict()
    assert result_dict == [
        {
            'xlink_type': 'resource',
            'xlink_label': 'label_AssetsAbstract',
            'xlink_role': 'http://www.xbrl.org/2003/role/label',
            'xml_lang': 'ja',
            'id': 'label_AssetsAbstract',
            'label': '資産の部',
            'xlink_schema': '../jppfs_cor_2022-11-01.xsd'
        },
        {
            'xlink_type': 'resource',
            'xlink_label': 'label_CurrentAssetsAbstract',
            'xlink_role': 'http://www.xbrl.org/2003/role/label',
            'xml_lang': 'ja',
            'id': 'label_CurrentAssetsAbstract',
            'label': '流動資産',
            'xlink_schema': '../jppfs_cor_2022-11-01.xsd'
        }
    ]
    # Remove the XML file
    # os.remove(xml_path)

def test_link_locs(label_parser):
    # Create a dummy XML with link:loc elements
    xml_content = """
<link:linkbase xmlns:link="http://www.xbrl.org/2003/linkbase" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xbrli="http://www.xbrl.org/2003/instance">
    <link:roleRef roleURI="http://disclosure.edinet-fsa.go.jp/jpcrp/std/alt/role/label" xlink:type="simple" xlink:href="../../../jpcrp/2022-11-01/jpcrp_rt_2022-11-01.xsd#rol_std_altLabel"/>
    <link:labelLink xlink:type="extended" xlink:role="http://www.xbrl.org/2003/role/link">
    <link:loc xlink:type="locator" xlink:href="../jppfs_cor_2022-11-01.xsd#jppfs_cor_AssetsAbstract" xlink:label="AssetsAbstract"/>
    <link:label xlink:type="resource" xlink:label="label_AssetsAbstract" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="ja" id="label_AssetsAbstract">資産の部</link:label>
    <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label" xlink:from="AssetsAbstract" xlink:to="label_AssetsAbstract"/>
    <link:loc xlink:type="locator" xlink:href="../jppfs_cor_2022-11-01.xsd#jppfs_cor_CurrentAssetsAbstract" xlink:label="CurrentAssetsAbstract"/>
    <link:label xlink:type="resource" xlink:label="label_CurrentAssetsAbstract" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="ja" id="label_CurrentAssetsAbstract">流動資産</link:label>
    <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label" xlink:from="CurrentAssetsAbstract" xlink:to="label_CurrentAssetsAbstract"/>
    </link:labelLink>
</link:linkbase>
    """
    # Set the BeautifulSoup object of the label_parser
    label_parser.soup = bs(xml_content, "xml")
    # Call the link_locs method
    result = label_parser.link_locs()
    # Check if the result is a LabelParser object
    assert isinstance(result, LabelParser)
    # Check if the data attribute is populated with the expected values
    assert result.data == [
        {
            'xlink_type': 'locator',
            'xlink_schema': '../jppfs_cor_2022-11-01.xsd',
            'xlink_href': 'jppfs_cor_AssetsAbstract',
            'xlink_label': 'AssetsAbstract'
        },
        {
            'xlink_type': 'locator',
            'xlink_schema': '../jppfs_cor_2022-11-01.xsd',
            'xlink_href': 'jppfs_cor_CurrentAssetsAbstract',
            'xlink_label': 'CurrentAssetsAbstract'
        }
    ]

def test_link_label_arcs(label_parser):
    # Create a dummy XML with link:labelArc elements
    xml_content = """
<link:linkbase xmlns:link="http://www.xbrl.org/2003/linkbase" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xbrli="http://www.xbrl.org/2003/instance">
  <link:roleRef roleURI="http://disclosure.edinet-fsa.go.jp/jpcrp/std/alt/role/label" xlink:type="simple" xlink:href="../../../jpcrp/2022-11-01/jpcrp_rt_2022-11-01.xsd#rol_std_altLabel"/>
    <link:labelLink xlink:type="extended" xlink:role="http://www.xbrl.org/2003/role/link">
    <link:loc xlink:type="locator" xlink:href="../jppfs_cor_2022-11-01.xsd#jppfs_cor_AssetsAbstract" xlink:label="AssetsAbstract"/>
    <link:label xlink:type="resource" xlink:label="label_AssetsAbstract" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="ja" id="label_AssetsAbstract">資産の部</link:label>
    <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label" xlink:from="AssetsAbstract" xlink:to="label_AssetsAbstract"/>
    <link:loc xlink:type="locator" xlink:href="../jppfs_cor_2022-11-01.xsd#jppfs_cor_CurrentAssetsAbstract" xlink:label="CurrentAssetsAbstract"/>
    <link:label xlink:type="resource" xlink:label="label_CurrentAssetsAbstract" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="ja" id="label_CurrentAssetsAbstract">流動資産</link:label>
    <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label" xlink:from="CurrentAssetsAbstract" xlink:to="label_CurrentAssetsAbstract"/>
  </link:labelLink>
</link:linkbase>
    """
    # Set the BeautifulSoup object of the label_parser
    label_parser.soup = bs(xml_content, "xml")
    # Call the link_label_arcs method
    result = label_parser.link_label_arcs()
    # Check if the result is a LabelParser object
    assert isinstance(result, LabelParser)
    # Check if the data attribute is populated with the expected values
    assert result.data == [
        {
            'xlink_type': 'arc',
            'xlink_arcrole': 'http://www.xbrl.org/2003/arcrole/concept-label',
            'xlink_from': 'AssetsAbstract',
            'xlink_to': 'label_AssetsAbstract',
            'xlink_schema': '../jppfs_cor_2022-11-01.xsd',
        },
        {
            'xlink_type': 'arc',
            'xlink_arcrole': 'http://www.xbrl.org/2003/arcrole/concept-label',
            'xlink_from': 'CurrentAssetsAbstract',
            'xlink_to': 'label_CurrentAssetsAbstract',
            'xlink_schema': '../jppfs_cor_2022-11-01.xsd',
        }
    ]

def test_role_refs(label_parser):
    # Create a dummy XML with roleRef elements
    xml_content = """
    <link:linkbase xmlns:link="http://www.xbrl.org/2003/linkbase" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xbrli="http://www.xbrl.org/2003/instance">
        <link:roleRef roleURI="http://disclosure.edinet-fsa.go.jp/jpcrp/std/alt/role/label" xlink:type="simple" xlink:href="../../../jpcrp/2022-11-01/jpcrp_rt_2022-11-01.xsd#rol_std_altLabel"/>
        <link:roleRef roleURI="http://disclosure.edinet-fsa.go.jp/jppfs/Consolidated/role/label" xlink:type="simple" xlink:href="../jppfs_rt_2022-11-01.xsd#rol_ConsolidatedLabel"/>
    </link:linkbase>
    """
    # Set the BeautifulSoup object of the label_parser
    label_parser.soup = bs(xml_content, "xml")
    # Call the role_refs method
    result = label_parser.role_refs()
    # Check if the result is a LabelParser object
    assert isinstance(result, LabelParser)
    # Check if the data attribute is populated with the expected values
    result_dict = result.to_dict()
    assert result.data == [
        {
            'Role_URI': 'http://disclosure.edinet-fsa.go.jp/jpcrp/std/alt/role/label',
            'xlink_type': 'simple',
            'xlink_schema': '../../../jpcrp/2022-11-01/jpcrp_rt_2022-11-01.xsd',
            'xlink_href': 'rol_std_altLabel'
        },
        {
            'Role_URI': 'http://disclosure.edinet-fsa.go.jp/jppfs/Consolidated/role/label',
            'xlink_type': 'simple',
            'xlink_schema': '../jppfs_rt_2022-11-01.xsd',
            'xlink_href': 'rol_ConsolidatedLabel'
        }
    ]