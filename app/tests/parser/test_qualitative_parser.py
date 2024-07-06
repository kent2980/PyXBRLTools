import pytest

from app.parser import QualitativeParser


@pytest.fixture
def get_output_dir(get_current_path):
    # Get the output directory path
    output_dir = get_current_path / "output"
    return output_dir.as_posix()


@pytest.fixture
def qualitative_parser(get_current_path):
    file_path = (
        get_current_path / "data" / "xbrl" / "edjp" / "Attachment" / "qualitative.htm"
    )
    parser = QualitativeParser.create(file_path.as_posix())
    return parser


def test_qualitative_info(qualitative_parser, get_output_dir):
    result = qualitative_parser.qualitative_info()
    assert isinstance(result.data, list)
    result.to_csv(get_output_dir + "/smt_head.csv")
    # assert len(result.to_DataFrame()) > 0
