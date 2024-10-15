import pprint
from pathlib import Path
from time import sleep

import pytest
import requests
from tqdm import tqdm

from app.ix_manager import (
    BaseXbrlManager,
    CalLinkManager,
    DefLinkManager,
    IXBRLManager,
    LabelManager,
    PreLinkManager,
)
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
                response = requests.post(urls[key], json={"data": value})
                assert response.status_code == 200
                flag = response.json()
                print(response.json())
            else:
                if flag:
                    assert isinstance(value, list)
                    try:
                        print(f"key: {key},{urls[key]}")
                        response = requests.post(
                            urls[key], json={"data": value}
                        )
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
                        json_item = (
                            {"data": item}
                            if isinstance(item, list)
                            else item
                        )
                        response = requests.post(url, json=json_item)
                        if not response.status_code == 200:
                            print(item[0])
                        assert response.status_code == 200


def test_fastapi(
    get_xbrl_zip_dir, get_output_dir, get_api_url, get_api_is
):

    base_url1 = "http://localhost:8000"

    base_url2 = "http://157.7.194.74"

    base_url3 = "https://api.fs-stock.net"

    url, is_url = None, None

    base_url = base_url1

    urls = get_api_url

    is_urls = get_api_is

    get_xbrl_zip_dir = "/Users/user/Documents/tdnet/xbrl/20240809"

    zips = list(Path(get_xbrl_zip_dir).rglob("*.zip"))

    with tqdm(total=len(zips)) as pbar:

        for model in XBRLModel.xbrl_models(
            get_xbrl_zip_dir, get_output_dir
        ):
            if model is None:
                pbar.update(1)
                continue

            items = model.get_all_items()

            data = {"xbrl_id": model.xbrl_id, "path": model.xbrl_zip_path}

            is_res = requests.get(
                f"{base_url}/api/v1/xbrl/ix/file_path/is/{model.xbrl_id}/"
            ).json()

            if not is_res:
                response = requests.post(
                    f"{base_url}/api/v1/xbrl/ix/file_path/", json=data
                )

                assert response.status_code == 200

            for item in items:
                # print(f"read item ***** [{item['key']}]")
                # if item["key"] == "qualitative_info":
                #     print(item)

                assert isinstance(item["id"], str)
                assert isinstance(item["key"], str)

                try:
                    url = f"{base_url}/{urls[item["key"]]}"
                    is_url = f"{base_url}/{is_urls[item["key"]]}"
                except KeyError as e:
                    continue

                is_add = requests.get(f"{is_url}{item["id"]}/").json()

                # if item["key"] == "qualitative_info":
                #     print(f"{is_url}{item["id"]}")
                #     print(is_add)

                if not is_add:
                    # print(f"add item ***** [{item['key']}]")
                    response = requests.post(
                        url, json={"data": item["item"]}
                    )

                    try:
                        response_json = response.json()
                    except requests.exceptions.JSONDecodeError as e:
                        print(item["item"])
                        print(f"JSONDecodeError: {e}")
                        print(f"Response content: {response.content}")
                        response_json = None

                    if not response.status_code == 200:
                        # print(model.xbrl_zip_path)
                        # pprint.pprint(item["item"])
                        pprint.pprint(response_json)

                    # assert response.status_code == 200

            pbar.update(1)
