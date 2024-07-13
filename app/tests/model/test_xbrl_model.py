import pprint

import pytest

from app.manager import (BaseXbrlManager, CalLinkManager, DefLinkManager,
                         IXBRLManager, LabelManager, PreLinkManager)
from app.models import XBRLModel
from app.tag import IxHeader


@pytest.fixture
def xbrl_model_edjp(get_xbrl_edjp_zip, get_output_dir):
    return XBRLModel(get_xbrl_edjp_zip, get_output_dir)


@pytest.fixture
def xbrl_model_rvfc(get_xbrl_rvfc_zip, get_output_dir):
    return XBRLModel(get_xbrl_rvfc_zip, get_output_dir)


def test_xbrl_model_instance(xbrl_model_edjp):
    assert isinstance(xbrl_model_edjp, XBRLModel)


def test_ixbrl_manager(xbrl_model_edjp):
    assert xbrl_model_edjp.ixbrl_manager is not None
    manager = xbrl_model_edjp.ixbrl_manager
    if manager:
        header = manager.get_ix_header()
        assert sorted(header.keys()) == sorted(IxHeader.keys())


def test_all_edjp(xbrl_model_edjp):
    model = xbrl_model_edjp
    assert model.xbrl_type == "edjp"
    assert isinstance(model.ixbrl_manager, IXBRLManager)
    assert isinstance(model.label_manager, LabelManager)
    assert isinstance(model.def_link_manager, DefLinkManager)
    assert isinstance(model.pre_link_manager, PreLinkManager)
    assert isinstance(model.cal_link_manager, CalLinkManager)

def test_xbrl_dir(get_xbrl_zip_dir, get_output_dir):
    XBRLModel.xbrl_models(get_xbrl_zip_dir, get_output_dir)
    for model in XBRLModel.xbrl_models(get_xbrl_zip_dir, get_output_dir):
        assert isinstance(model, XBRLModel)
        print(model.xbrl_type)
        for _, manager in model.get_all_manager().items():
            assert manager is not None
            assert isinstance(manager, BaseXbrlManager)
            for key, item in manager.items.items():
                if key == "ix_header":
                    print(item)

def test_api_insert(get_xbrl_zip_dir, get_output_dir):
    pass
