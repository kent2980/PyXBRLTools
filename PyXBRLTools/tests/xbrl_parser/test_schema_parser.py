import pytest
from bs4 import BeautifulSoup as bs

from PyXBRLTools.xbrl_parser.schema_parser import SchemaParser


@pytest.fixture
def schema_parser():
    xbrl_content = """<xbrl>
    <import schemaLocation="schema1.xsd" namespace="ns1"/>
    <import schemaLocation="schema2.xsd" namespace="ns2"/>
    </xbrl>"""
    xbrl_url = "http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2022-11-01/jpcrp_cor_2022-11-01.xsd"
    output_dir = "output"
    soup = bs(xbrl_content, "xml")
    schema_parser = SchemaParser(xbrl_url, output_dir)
    schema_parser.soup = soup
    return schema_parser


def test_import_schemas(schema_parser):
    result = schema_parser.import_schemas()
    assert isinstance(result.data, list)
    assert len(result.data) == 2
    assert result.data[0] == {
        "document_type": "sm",
        "schema_location": "schema1.xsd",
        "name_space": "ns1",
    }
    assert result.data[1] == {
        "document_type": "sm",
        "schema_location": "schema2.xsd",
        "name_space": "ns2",
    }


def test_link_base_refs(schema_parser):
    result = schema_parser.link_base_refs()
    assert isinstance(result.data, list)
    assert len(result.data) == 0


def test_elements(schema_parser):
    result = schema_parser.elements()
    assert isinstance(result.data, list)
    assert len(result.data) == 0
