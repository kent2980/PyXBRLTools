import pytest
from bs4 import BeautifulSoup as bs
from PyXBRLTools.xbrl_parser.qualitative_parser import QualitativeParser
from PyXBRLTools.tests.xbrl_manager.test_base_xbrl_manager import get_current_dir
from pathlib import Path
from PyXBRLTools.tests.xbrl_manager.test_label_manager import get_output_dir

def get_current_dir():
    # Get the current directory path
    current_dir = Path(__file__).resolve().parent.parent
    return current_dir

def get_output_dir():
    # Get the output directory path
    output_dir = get_current_dir() / "output"
    return output_dir.as_posix()

@pytest.fixture
def qualitative_parser():
    file_path = get_current_dir() / "data" / "edjp" / "Attachment" / "qualitative.htm"
    parser = QualitativeParser.create(file_path.as_posix())
    return parser

def test_smt_head(qualitative_parser):
    result = qualitative_parser.smt_head()
    assert isinstance(result.data, list)
    result.to_csv(get_output_dir() + "/smt_head.csv")
    assert len(result.to_DataFrame()) > 0