from litestar import get, Response, MediaType
from litestar.testing import create_test_client

from stubborn import Stubborn

REGISTER_RESULT = {"result": "success"}


def test_sanity():
    with create_test_client([Stubborn]) as client:
        res = client.get("/")
        assert res.status_code == 404

        expected_response_1 = {"result": "success"}
        path = "/test"
        res = client.post(
            "/_register", json={"path": path, "method": "GET", "count": 1, "response": expected_response_1}
        )
        assert res.status_code == 201
        assert res.json() == REGISTER_RESULT


def test_register_with_count():
    with create_test_client([Stubborn]) as client:
        expected_response_1 = {"result": "success"}
        path = "/test"
        res = client.post(
            "/_register", json={"path": path, "method": "GET", "count": 1, "response": expected_response_1}
        )
        assert res.status_code == 201
        assert res.json() == REGISTER_RESULT
        res = client.get(path)
        assert res.status_code == 200
        assert res.json() == expected_response_1
        res = client.get(path)
        assert res.status_code == 404


def test_register_without_count():
    with create_test_client([Stubborn]) as client:
        expected_response_1 = {"result": "success"}
        path = "/test"
        client.post("/_register", json={"path": path, "method": "GET", "response": expected_response_1})
        for i in range(13):
            res = client.get(path)
            assert res.status_code == 200
            assert res.json() == expected_response_1


def test_register_with_status_code():
    with create_test_client([Stubborn]) as client:
        expected_response_1 = {"result": "success"}
        path = "/test"
        status_code = 201
        client.post(
            "/_register",
            json={
                "path": path,
                "method": "GET",
                "count": 1,
                "response": expected_response_1,
                "status_code": status_code,
            },
        )
        res = client.get(path)
        assert res.status_code == status_code
        assert res.json() == expected_response_1


def test_register_with_different_methods():
    with create_test_client([Stubborn]) as client:
        expected_response_1 = {"result": "success"}
        path = "/test"
        client.post(
            "/_register",
            json={
                "path": path,
                "method": "POST",
                "count": 1,
                "response": expected_response_1,
            },
        )
        res = client.get(path)
        assert res.status_code == 404
        res = client.post(path)
        assert res.status_code == 200
        assert res.json() == expected_response_1


def test_register_multiple_paths():
    with create_test_client([Stubborn]) as client:
        expected_response_1 = {"result": "success"}
        expected_response_2 = {"result": "success2"}
        path_1 = "/test"
        path_2 = "/test2"
        client.post("/_register", json={"path": path_1, "method": "GET", "count": 1, "response": expected_response_1})
        client.post("/_register", json={"path": path_2, "method": "GET", "count": 1, "response": expected_response_2})
        res = client.get(path_1)
        assert res.status_code == 200
        assert res.json() == expected_response_1
        res = client.get(path_1)
        assert res.status_code == 404
        res = client.get(path_2)
        assert res.status_code == 200
        assert res.json() == expected_response_2
