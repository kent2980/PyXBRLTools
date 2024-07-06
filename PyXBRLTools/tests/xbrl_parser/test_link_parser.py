import pytest
from bs4 import BeautifulSoup as bs

from PyXBRLTools.xbrl_parser.link_parser import PreLinkParser


@pytest.fixture
def pre_link_parser() -> PreLinkParser:
    xbrl_url = "http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2022-11-01/jpcrp_cor_2022-11-01_pre.xml"
    output_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/TEST"
    return PreLinkParser(xbrl_url, output_path)


def pre_link_content():
    content = """
<link:linkbase xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:link="http://www.xbrl.org/2003/linkbase">
  <link:roleRef xlink:type="simple" xlink:href="http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2022-11-01/jppfs_rt_2022-11-01.xsd#rol_QuarterlyConsolidatedBalanceSheet" roleURI="http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_QuarterlyConsolidatedBalanceSheet" />
  <link:roleRef xlink:type="simple" xlink:href="http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2022-11-01/jppfs_rt_2022-11-01.xsd#rol_YearToQuarterEndConsolidatedStatementOfComprehensiveIncome" roleURI="http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_YearToQuarterEndConsolidatedStatementOfComprehensiveIncome" />
  <link:roleRef xlink:type="simple" xlink:href="http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2022-11-01/jppfs_rt_2022-11-01.xsd#rol_YearToQuarterEndConsolidatedStatementOfIncome" roleURI="http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_YearToQuarterEndConsolidatedStatementOfIncome" />
  <link:roleRef xlink:type="simple" xlink:href="http://www.xbrl.tdnet.info/taxonomy/jp/tse/tdnet/at/o/rt/2014-01-12/tse-at-rt-2014-01-12.xsd#RoleAttachedDocument" roleURI="http://www.xbrl.tdnet.info/jp/tse/tdnet/role/RoleAttachedDocument" />
  <link:presentationLink xlink:type="extended" xlink:role="http://www.xbrl.tdnet.info/jp/tse/tdnet/role/RoleAttachedDocument">
    <link:loc xlink:type="locator" xlink:href="http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2022-11-01/jpcrp_cor_2022-11-01.xsd#jpcrp_cor_QuarterlyConsolidatedBalanceSheetTextBlock" xlink:label="jpcrp_cor_QuarterlyConsolidatedBalanceSheetTextBlock" />
    <link:loc xlink:type="locator" xlink:href="http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2022-11-01/jpcrp_cor_2022-11-01.xsd#jpcrp_cor_QuarterlyConsolidatedFinancialStatementsHeading" xlink:label="jpcrp_cor_QuarterlyConsolidatedFinancialStatementsHeading" />
    <link:presentationArc xlink:type="arc" xlink:from="jpcrp_cor_QuarterlyConsolidatedFinancialStatementsHeading" xlink:to="jppfs_cor_QuarterlyConsolidatedBalanceSheetHeading" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child" order="1" />
    <link:presentationArc xlink:type="arc" xlink:from="jpcrp_cor_QuarterlyConsolidatedFinancialStatementsHeading" xlink:to="jppfs_cor_QuarterlyConsolidatedStatementOfIncomeAndConsolidatedStatementOfComprehensiveIncomeHeading" xlink:arcrole="http://www.xbrl.org/2003/arcrole/parent-child" order="2" />
  </link:presentationLink>
</link:linkbase>
    """
    return content


def test_link_roles(pre_link_parser):
    # Test link_roles method
    pre_link_parser.soup = bs(pre_link_content(), "xml")
    result = pre_link_parser.link_roles()
    assert isinstance(result, PreLinkParser)
    assert result.to_dict() == [
        {
            "xlink_type": "simple",
            "xlink_href": "http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2022-11-01/jppfs_rt_2022-11-01.xsd#rol_QuarterlyConsolidatedBalanceSheet",
            "role_uri": "http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_QuarterlyConsolidatedBalanceSheet",
        },
        {
            "xlink_type": "simple",
            "xlink_href": "http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2022-11-01/jppfs_rt_2022-11-01.xsd#rol_YearToQuarterEndConsolidatedStatementOfComprehensiveIncome",
            "role_uri": "http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_YearToQuarterEndConsolidatedStatementOfComprehensiveIncome",
        },
        {
            "xlink_type": "simple",
            "xlink_href": "http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2022-11-01/jppfs_rt_2022-11-01.xsd#rol_YearToQuarterEndConsolidatedStatementOfIncome",
            "role_uri": "http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_YearToQuarterEndConsolidatedStatementOfIncome",
        },
        {
            "xlink_type": "simple",
            "xlink_href": "http://www.xbrl.tdnet.info/taxonomy/jp/tse/tdnet/at/o/rt/2014-01-12/tse-at-rt-2014-01-12.xsd#RoleAttachedDocument",
            "role_uri": "http://www.xbrl.tdnet.info/jp/tse/tdnet/role/RoleAttachedDocument",
        },
    ]


def test_link_locs(pre_link_parser):
    # Test link_locs method
    pre_link_parser.soup = bs(pre_link_content(), "xml")
    result = pre_link_parser.link_locs()
    assert isinstance(result, PreLinkParser)
    assert result.to_dict() == [
        {
            "attr_value": "http://www.xbrl.tdnet.info/jp/tse/tdnet/role/RoleAttachedDocument",
            "xlink_type": "locator",
            "xlink_schema": "http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2022-11-01/jpcrp_cor_2022-11-01.xsd",
            "xlink_href": "jpcrp_cor_QuarterlyConsolidatedBalanceSheetTextBlock",
            "xlink_label": "jpcrp_cor_QuarterlyConsolidatedBalanceSheetTextBlock",
        },
        {
            "attr_value": "http://www.xbrl.tdnet.info/jp/tse/tdnet/role/RoleAttachedDocument",
            "xlink_type": "locator",
            "xlink_schema": "http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2022-11-01/jpcrp_cor_2022-11-01.xsd",
            "xlink_href": "jpcrp_cor_QuarterlyConsolidatedFinancialStatementsHeading",
            "xlink_label": "jpcrp_cor_QuarterlyConsolidatedFinancialStatementsHeading",
        },
    ]


def test_link_arcs(pre_link_parser):
    # Test link_arcs method
    pre_link_parser.soup = bs(pre_link_content(), "xml")
    result = pre_link_parser.link_arcs()
    assert isinstance(result, PreLinkParser)
    assert result.to_dict() == [
        {
            "attr_value": "http://www.xbrl.tdnet.info/jp/tse/tdnet/role/RoleAttachedDocument",
            "xlink_type": "arc",
            "xlink_arcrole": "http://www.xbrl.org/2003/arcrole/parent-child",
            "xlink_from": "jpcrp_cor_QuarterlyConsolidatedFinancialStatementsHeading",
            "xlink_to": "jppfs_cor_QuarterlyConsolidatedBalanceSheetHeading",
            "xlink_order": 1,
            "xlink_weight": None,
        },
        {
            "attr_value": "http://www.xbrl.tdnet.info/jp/tse/tdnet/role/RoleAttachedDocument",
            "xlink_type": "arc",
            "xlink_arcrole": "http://www.xbrl.org/2003/arcrole/parent-child",
            "xlink_from": "jpcrp_cor_QuarterlyConsolidatedFinancialStatementsHeading",
            "xlink_to": "jppfs_cor_QuarterlyConsolidatedStatementOfIncomeAndConsolidatedStatementOfComprehensiveIncomeHeading",
            "xlink_order": 2,
            "xlink_weight": None,
        },
    ]


def test_link_base(pre_link_parser):
    # Test link_base method
    pre_link_parser.soup = bs(pre_link_content(), "xml")
    result = pre_link_parser.link_base()
    assert isinstance(result, PreLinkParser)
    assert result.to_dict() == [
        {
            "xmlns_xlink": "http://www.w3.org/1999/xlink",
            "xmlns_xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns_link": "http://www.xbrl.org/2003/linkbase",
        }
    ]


def test_calculationLink(pre_link_parser):
    # Test calculationLink method
    pre_link_parser.soup = bs(pre_link_content(), "xml")
    result = pre_link_parser.link()
    assert isinstance(result, PreLinkParser)
    assert result.to_dict() == [
        {
            "xlink_type": "extended",
            "xlink_role": "http://www.xbrl.tdnet.info/jp/tse/tdnet/role/RoleAttachedDocument",
        }
    ]
