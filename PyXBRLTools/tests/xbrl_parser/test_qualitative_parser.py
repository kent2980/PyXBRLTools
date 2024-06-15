import pytest
from bs4 import BeautifulSoup as bs
from PyXBRLTools.xbrl_parser.qualitative_parser import QualitativeParser

@pytest.fixture
def qualitative_parser():
    xbrl_content = """
    <html>
        <body>
            <div class="smt_head1">Head 1</div>
            <div class="smt_head2">Head 2</div>
            <div class="smt_text">Text 1</div>
            <div class="smt_text">Text 2</div>
            <div class="smt_head1">Head 1</div>
            <div class="smt_head2">Head 2</div>
            <div class="smt_text">Text 3</div>
        </body>
    </html>
    """
    soup = bs(xbrl_content, "html.parser")
    xbrl_path = "qualitative.htm"
    output_dir = "output"
    qualitative_parser:QualitativeParser = QualitativeParser(xbrl_path, output_dir)
    qualitative_parser.soup = soup
    return qualitative_parser

def test_smt_head(qualitative_parser):
    result = qualitative_parser.smt_head()
    assert isinstance(result.data, list)
    assert len(result.data) > 0
    assert result.data[0] == {'title': 'Head 1', 'sub_title': 'Head 2', 'text': 'Text 1Text 2Text 3'}