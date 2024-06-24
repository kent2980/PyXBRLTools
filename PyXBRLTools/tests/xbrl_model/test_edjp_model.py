import pytest
from pathlib import Path
from PyXBRLTools.xbrl_model.edjp_model import EdjpModel
from PyXBRLTools.xbrl_exception.xbrl_model_exception import NotXbrlTypeException
from PyXBRLTools.xbrl_model.base_xbrl_model import BaseXbrlModel

@pytest.fixture
def edjp_model(get_current_path):
    zip_dir = get_current_path / "data" / "xbrl_zip"
    zip_name = "edjp.zip"
    zip_path = zip_dir / zip_name
    output_path = get_current_path / "data" / "output"
    return EdjpModel(zip_path.as_posix(), output_path.as_posix())

def test_edjp_model_initialization(edjp_model):
    assert isinstance(edjp_model, EdjpModel)

def test_edjp_model_inherits_base_xbrl_model(edjp_model):
    assert isinstance(edjp_model, BaseXbrlModel)

def test_edjp_model_raises_exception_for_invalid_xbrl_type(get_current_path):
    zip_dir = get_current_path / "data" / "xbrl_zip"
    zip_name = "rvfc.zip"
    zip_path = zip_dir / zip_name
    output_path = get_current_path / "data" / "output"
    with pytest.raises(NotXbrlTypeException):
        EdjpModel(zip_path.as_posix(), output_path.as_posix())

def test_edjp_model_check_folder_structure(edjp_model):
    key = ("ixbrl.htm", "lab", "pre", "cal", "def")
    assert edjp_model._BaseXbrlModel__check_xbrl_files_in_dir(*key)

def test_get_ixbrl(edjp_model):
    ix_non_fraction, ix_non_numeric = edjp_model.get_ixbrl()
    assert not ix_non_fraction.empty
    assert not ix_non_numeric.empty

def test_get_label(edjp_model):
    locs, arcs, labels = edjp_model.get_label()
    assert not locs.empty
    assert not arcs.empty
    assert not labels.empty

def test_get_cal_linkbase(edjp_model):
    locs, arcs = edjp_model.get_cal_linkbase()
    assert not locs.empty
    assert not arcs.empty

def test_get_pre_linkbase(edjp_model):
    locs, arcs = edjp_model.get_pre_linkbase()
    assert not locs.empty
    assert not arcs.empty

def test_get_def_linkbase(edjp_model):
    locs, arcs = edjp_model.get_def_linkbase()
    assert not locs.empty
    assert not arcs.empty
