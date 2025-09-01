import random
from uuid import uuid4
from fastapi.testclient import TestClient
from app.core.config import settings
from httpx import Response
import pytest

countries_url = "/".join([settings.API_V1_STR, "countries"])
expected_keys = {"id", "iso", "name", "nice_name", "iso3", "num_code", "phone_code"}


@pytest.fixture
def countries_response(client: TestClient) -> Response:
    return client.get(countries_url)


def test_get_countries_status_code(countries_response: Response):
    assert countries_response.status_code == 200


def test_get_countries_structure(countries_response: Response):
    json_data = countries_response.json()

    assert "data" in json_data
    assert "count" in json_data
    assert isinstance(json_data["data"], list)
    assert isinstance(json_data["count"], int)


def test_get_countries_data_item_structure(countries_response: Response):
    item = countries_response.json()["data"][0]
    assert set(item.keys()) == expected_keys


def test_get_countries_data_types(countries_response: Response):
    item = countries_response.json()["data"][0]
    fields_types = [
        ("id", str),
        ("iso", str),
        ("name", str),
        ("nice_name", str),
        ("iso3", str),
        ("num_code", int),
        ("phone_code", int),
    ]
    for field, typ in fields_types:
        assert isinstance(item[field], typ)

    from uuid import UUID

    try:
        UUID(item["id"])
    except Exception:
        pytest.fail("El campo 'id' no es un UUID válido")


def test_get_country_status_code(client: TestClient, countries_response: Response):
    json_data = countries_response.json()["data"]
    random_country = random.choice(json_data)
    response = client.get("/".join([countries_url, random_country["id"]]))
    assert response.status_code == 200


def test_get_country_structure(client: TestClient, countries_response: Response):
    json_data = countries_response.json()["data"]
    random_country = random.choice(json_data)
    response = client.get("/".join([countries_url, random_country["id"]]))
    assert set(response.json().keys()) == expected_keys


def test_get_not_found_country(client: TestClient, countries_response: Response):
    response = client.get("/".join([countries_url, uuid4().__str__()]))
    assert response.status_code == 404
    json_data = response.json()
    assert "detail" in json_data
