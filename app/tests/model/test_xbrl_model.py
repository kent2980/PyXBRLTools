import pprint

import pytest

from app.manager import (CalLinkManager, DefLinkManager, IXBRLManager,
                         LabelManager, PreLinkManager)
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
    assert isinstance(model.ixbrl_manager, IXBRLManager)
    assert isinstance(model.label_manager, LabelManager)
    assert isinstance(model.def_link_manager, DefLinkManager)
    assert isinstance(model.pre_link_manager, PreLinkManager)
    assert isinstance(model.cal_link_manager, CalLinkManager)
    print(
        f"\n*****[test_all_{model.xbrl_type}] model.get_all_manager()"
        + "*" * 50
        + "\n"
    )
    for key, value in model.get_all_manager().items():
        print(f"<{key}>")
        print(value)

        # IxbrlManager
        if isinstance(value, IXBRLManager):
            assert isinstance(value, IXBRLManager)
            pprint.pprint(value.get_ix_header())
            for item in value.get_ix_non_fraction():
                pprint.pprint(item)
            for item in value.get_ix_non_fraction():
                pprint.pprint(item)

        # LabelManager
        elif isinstance(value, LabelManager):
            assert isinstance(value, LabelManager)
            for item in value.get_link_labels():
                pprint.pprint(item)
            for item in value.get_link_label_locs():
                pprint.pprint(item)
            for item in value.get_link_label_arcs():
                pprint.pprint(item)

        # DefLinkManager
        elif isinstance(value, DefLinkManager):
            for item in value.get_link_roles():
                pprint.pprint(item)
            for item in value.get_link_arcs():
                pprint.pprint(item)
            for item in value.get_link_locs():
                pprint.pprint(item)
            assert isinstance(value, DefLinkManager)

        # PreLinkManager
        elif isinstance(value, PreLinkManager):
            for item in value.get_link_roles():
                pprint.pprint(item)
            for item in value.get_link_arcs():
                pprint.pprint(item)
            for item in value.get_link_locs():
                pprint.pprint(item)
            assert isinstance(value, PreLinkManager)

        # CalLinkManager
        elif isinstance(value, CalLinkManager):
            for item in value.get_link_roles():
                pprint.pprint(item)
            for item in value.get_link_arcs():
                pprint.pprint(item)
            for item in value.get_link_locs():
                pprint.pprint(item)
            assert isinstance(value, CalLinkManager)


def test_all_rvfc(xbrl_model_rvfc):
    model = xbrl_model_rvfc
    assert isinstance(model, XBRLModel)
    xbrl_id = model.xbrl_id
    print(
        f"\n*****[test_all_{model.xbrl_type}] model.get_all_manager()"
        + "*" * 50
        + "\n"
    )
    for key, value in model.get_all_manager().items():
        print(f"<{key}>")
        print(value)

        # IxbrlManager
        if isinstance(value, IXBRLManager):
            assert isinstance(value, IXBRLManager)
            pprint.pprint(value.get_ix_header())
            for item in value.get_ix_non_fraction():
                pprint.pprint(item)
                assert [xbrl_id == i["xbrl_id"] for i in item]
            for item in value.get_ix_non_fraction():
                pprint.pprint(item)
                assert [xbrl_id == i["xbrl_id"] for i in item]

        # LabelManager
        elif isinstance(value, LabelManager):
            assert isinstance(value, LabelManager)
            for item in value.get_link_labels():
                pprint.pprint(item)
            for item in value.get_link_label_locs():
                pprint.pprint(item)
            for item in value.get_link_label_arcs():
                pprint.pprint(item)

        # DefLinkManager
        elif isinstance(value, DefLinkManager):
            for item in value.get_link_roles():
                pprint.pprint(item)
                assert [xbrl_id == i["xbrl_id"] for i in item]
            for item in value.get_link_arcs():
                pprint.pprint(item)
                assert [xbrl_id == i["xbrl_id"] for i in item]
            for item in value.get_link_locs():
                pprint.pprint(item)
                assert [xbrl_id == i["xbrl_id"] for i in item]
            assert isinstance(value, DefLinkManager)

        # PreLinkManager
        elif isinstance(value, PreLinkManager):
            for item in value.get_link_roles():
                pprint.pprint(item)
                assert [xbrl_id == i["xbrl_id"] for i in item]
            for item in value.get_link_arcs():
                pprint.pprint(item)
                assert [xbrl_id == i["xbrl_id"] for i in item]
            for item in value.get_link_locs():
                pprint.pprint(item)
                assert [xbrl_id == i["xbrl_id"] for i in item]
            assert isinstance(value, PreLinkManager)

        # CalLinkManager
        elif isinstance(value, CalLinkManager):
            for item in value.get_link_roles():
                pprint.pprint(item)
                assert [xbrl_id == i["xbrl_id"] for i in item]
            for item in value.get_link_arcs():
                pprint.pprint(item)
                assert [xbrl_id == i["xbrl_id"] for i in item]
            for item in value.get_link_locs():
                pprint.pprint(item)
                assert [xbrl_id == i["xbrl_id"] for i in item]
            assert isinstance(value, CalLinkManager)

def test_xbrl_models(get_xbrl_zip_dir, get_output_dir):
    for model in XBRLModel.xbrl_models(get_xbrl_zip_dir, get_output_dir):
        assert isinstance(model, XBRLModel)
        print(
            f"\n*****[test_xbrl_models] model.get_all_manager()"
            + "*" * 50
            + "\n"
        )
        for key, value in model.get_all_manager().items():
            print(f"<{key}>")
            print(value)

            # IxbrlManager
            if isinstance(value, IXBRLManager):
                assert isinstance(value, IXBRLManager)
                pprint.pprint(value.get_ix_header())
                for item in value.get_ix_non_fraction():
                    pprint.pprint(item)
                for item in value.get_ix_non_fraction():
                    pprint.pprint(item)

            # LabelManager
            elif isinstance(value, LabelManager):
                assert isinstance(value, LabelManager)
                for item in value.get_link_labels():
                    pprint.pprint(item)
                for item in value.get_link_label_locs():
                    pprint.pprint(item)
                for item in value.get_link_label_arcs():
                    pprint.pprint(item)

            # DefLinkManager
            elif isinstance(value, DefLinkManager):
                for item in value.get_link_roles():
                    pprint.pprint(item)
                for item in value.get_link_arcs():
                    pprint.pprint(item)
                for item in value.get_link_locs():
                    pprint.pprint(item)
                assert isinstance(value, DefLinkManager)

            # PreLinkManager
            elif isinstance(value, PreLinkManager):
                for item in value.get_link_roles():
                    pprint.pprint(item)
                for item in value.get_link_arcs():
                    pprint.pprint(item)
                for item in value.get_link_locs():
                    pprint.pprint(item)
                assert isinstance(value, PreLinkManager)

            # CalLinkManager
            elif isinstance(value, CalLinkManager):
                for item in value.get_link_roles():
                    pprint.pprint(item)
                for item in value.get_link_arcs():
                    pprint.pprint(item)
                for item in value.get_link_locs():
                    pprint.pprint(item)
                assert isinstance(value, CalLinkManager)
