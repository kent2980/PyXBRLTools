import pprint
from time import sleep

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


def test_api_insert(get_xbrl_zip_dir, get_output_dir, get_api_url):

    urls = get_api_url

    for model in XBRLModel.xbrl_models(get_xbrl_zip_dir, get_output_dir):
        print(model)
        for key, value in model.get_all_items().items():
            flag = True
            if "source" in key:
                assert "source" in key
                print(f"key: {key},{urls[key]}")
                # pprint.pprint(value)
                response = requests.post(urls[key], json={"data":value})
                assert response.status_code == 200
                flag = response.json()
                print(response.json())
            else:
                if flag:
                    assert isinstance(value, list)
                    try:
                        print(f"key: {key},{urls[key]}")
                        response = requests.post(urls[key], json={"data":value})
                        print(response.json())
                        assert response.status_code == 200
                        # if "linkbase" in key:
                            # pprint.pprint(value)
                    except KeyError as e:
                        print(e)

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

def test_items(get_xbrl_zip_dir, get_output_dir, get_api_url, get_api_is):

    urls = get_api_url

    is_urls = get_api_is

    for model in XBRLModel.xbrl_models(get_xbrl_zip_dir, get_output_dir):
        items = model.get_all_items()
        print("*" * 100)
        # print(model)
        for key, value in items.items():
            try:
                url = urls[key]
            except KeyError as e:
                continue
            # assert isinstance(value, list)
            for items in value:
                # assert isinstance(items, dict)
                for sc_id, item in items.items():
                    print(f"{sc_id},key:{key} , {len(item)}")
                    # if len(item) > 0:
                    is_url = f"{is_urls[key]}{sc_id}"
                    print(is_url)
                    is_add = requests.get(is_url).json()
                    print(is_add)
                    if not is_add:
                        print(f"add item ***** [{sc_id}]")
                        print(url)
                        assert isinstance(item[0], dict)
                        json_item = {"data":item} if isinstance(item, list) else item
                        response = requests.post(url, json=json_item)
                        if not response.status_code == 200:
                            print(item[0])
                        assert response.status_code == 200

def test_sf_id_list(get_xbrl_zip_dir, get_output_dir, get_api_url, get_api_is):

    url, is_url = None, None

    urls = get_api_url

    is_urls = get_api_is

    get_xbrl_zip_dir = "/Users/user/Documents/tdnet/xbrl"

    for model in XBRLModel.xbrl_models(get_xbrl_zip_dir, get_output_dir):
        print(model.xbrl_zip_path)
        print(model)
        items = model.get_all_items()
        for item in items:
            assert isinstance(item["item"], list)
            assert isinstance(item["id"], str)
            assert isinstance(item["key"], str)

            try:
                url = urls[item["key"]]
                is_url = is_urls[item["key"]]
            except KeyError as e:
                continue

            print(f"{item["id"]}, {item["key"]}, type:{type(item["item"])}, {len(item["item"])}")

            print(url)

            print(is_url)

            is_add = requests.get(f"{is_url}{item["id"]}/").json()

            print(is_add)
            # assert is_add
            if not is_add:
                response = requests.post(url, json={"data":item["item"]})

                if not response.status_code == 200:
                    pprint.pprint(item["item"])

                # print(response.json())
                assert response.status_code == 200
