import pprint

import pytest
import requests

from app.ix_manager import (BaseXbrlManager, CalLinkManager, DefLinkManager,
                            IXBRLManager, LabelManager, PreLinkManager)
from app.ix_models import XBRLModel
from app.ix_tag import IxHeader


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
        print("\n" + model.xbrl_type)
        for _, manager in model.get_all_manager().items():
            assert manager is not None
            assert isinstance(manager, BaseXbrlManager)
            for key, item in manager.items.items():
                if key == "ix_header":
                    pprint.pprint(item)
                if key == "ix_context":
                    # pprintで要素間に空白を入れる
                    pprint.pprint(item)


def test_head_title_api_insert(get_xbrl_zip_dir, get_output_dir):
    XBRLModel.xbrl_models(get_xbrl_zip_dir, get_output_dir)
    for model in XBRLModel.xbrl_models(get_xbrl_zip_dir, get_output_dir):
        for value in model.get_all_manager().values():
            if isinstance(value, IXBRLManager):
                ix_non_fraction = value.ix_header
                # apiにデータを送信
                url = "http://localhost/api/v1/xbrls/head/"
                print(ix_non_fraction)
                response = requests.post(
                    url,
                    json=ix_non_fraction,
                )
                print(response.json())
                assert response.status_code == 200


def test_non_fraction_api_insert(get_xbrl_zip_dir, get_output_dir):
    XBRLModel.xbrl_models(get_xbrl_zip_dir, get_output_dir)
    for model in XBRLModel.xbrl_models(get_xbrl_zip_dir, get_output_dir):
        for value in model.get_all_manager().values():
            if isinstance(value, IXBRLManager):
                header = value.ix_header
                url = "http://localhost/api/v1/xbrl/ix/head/"
                response = requests.post(
                    url,
                    json=header,
                )
                print(response.json())
                assert response.status_code == 200
                ix_non_fraction = value.ix_non_fraction
                for items in ix_non_fraction:
                    for item in items:
                        # apiにデータを送信
                        url = (
                            "http://localhost/api/v1/xbrl/ix/non_fraction/"
                        )
                        pprint.pprint(item)
                        response = requests.post(
                            url,
                            json=item,
                        )
                        print(response.json())
                        assert response.status_code == 200


def test_all_managers(get_xbrl_zip_dir, get_output_dir):
    for model in XBRLModel.xbrl_models(get_xbrl_zip_dir, get_output_dir):
        for key, value in model.get_all_manager().items():
            print(key)


def test_non_numeric_api_insert(get_xbrl_zip_dir, get_output_dir):
    url_base = "http://localhost/api/v1/xbrl"
    urls = {
        "ix_header": f"{url_base}/ix/head/",
        "ix_non_fraction": f"{url_base}/ix/non_fraction/list/",
        "ix_non_numeric": f"{url_base}/ix/non_numeric/list/",
        "ix_source_files": f"{url_base}/source/list/",
        # 'ix_context': f'{url_base}/ix/context/',
        "lab_link_locs": f"{url_base}/link/lab/loc/list/all/",
        "lab_link_arcs": f"{url_base}/link/lab/arc/list/all/",
        "lab_link_values": f"{url_base}/link/lab/value/list/all/",
        "lab_source_files": f"{url_base}/source/list/",
        # 'cal_link_roles': f'{url_base}/link/cal/role/',
        "cal_link_locs": f"{url_base}/link/cal/loc/list/",
        "cal_link_arcs": f"{url_base}/link/cal/arc/list/",
        "cal_source_files": f"{url_base}/source/list/",
        # 'def_link_roles': f'{url_base}/link/def/role/',
        "def_link_locs": f"{url_base}/link/def/loc/list/",
        "def_link_arcs": f"{url_base}/link/def/arc/list/",
        "def_source_files": f"{url_base}/source/list/",
        # 'pre_link_roles': f'{url_base}/link/pre/role/',
        "pre_link_locs": f"{url_base}/link/pre/loc/list/",
        "pre_link_arcs": f"{url_base}/link/pre/arc/list/",
        "pre_source_files": f"{url_base}/source/list/",
    }
    for model in XBRLModel.xbrl_models(get_xbrl_zip_dir, get_output_dir):
        print(model)
        head = model.get_ixbrl().ix_header
        url = urls["ix_header"]
        print(url)
        print(head)
        # response = requests.post(s
        items = model.get_all_items()
        for key, value in items.items():
            if isinstance(value, list):
                if "source" in key:
                    for items in value:
                        url = urls[key]
                        print(url)
                        response = requests.post(
                            url,
                            json={"data": items},
                        )
                        result = response.json()
                        assert response.status_code == 200
                if result != "Items already exists":
                    if (
                        "ix" in key
                        or "cal" in key
                        or "def" in key
                        or "pre" in key
                        or "lab" in key
                    ):
                        for items in value:
                            try:
                                url = urls[key]
                                print(url)
                                response = requests.post(
                                    url,
                                    json={"data": items},
                                )
                                print(response.json())
                                assert response.status_code == 200
                            except KeyError:
                                continue


def test_xbrl_id_equal(get_xbrl_zip_dir, get_output_dir):
    for model in XBRLModel.xbrl_models(get_xbrl_zip_dir, get_output_dir):
        ix_header = model.get_ixbrl().ix_header
        print(ix_header)
        for key, value in model.get_all_items().items():
            if isinstance(value, list):
                for items in value:
                    for item in items:
                        if isinstance(item, dict):
                            if "xbrl_id" in item:
                                print(key)
                                print(item["xbrl_id"])
                                # assert xbrl_id == item["xbrl_id"]
        break
