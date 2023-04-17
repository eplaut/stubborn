from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED


REGISTER_RESULT = {"result": "success"}


def test_sanity(test_client):
    res = test_client.get("/")
    assert res.status_code == HTTP_404_NOT_FOUND

    expected_response_1 = {"result": "success"}
    path = "/test"
    res = test_client.post(
        "/_register", json={"path": path, "method": "GET", "count": 1, "response": expected_response_1}
    )
    assert res.status_code == HTTP_201_CREATED
    assert res.json() == REGISTER_RESULT


def test_register_with_count(test_client):
    expected_response_1 = {"result": "success"}
    path = "/test"
    res = test_client.post(
        "/_register", json={"path": path, "method": "GET", "count": 1, "response": expected_response_1}
    )
    assert res.status_code == HTTP_201_CREATED
    assert res.json() == REGISTER_RESULT
    res = test_client.get(path)
    assert res.status_code == HTTP_200_OK
    assert res.json() == expected_response_1
    res = test_client.get(path)
    assert res.status_code == HTTP_404_NOT_FOUND


def test_register_without_count(test_client):
    expected_response_1 = {"result": "success"}
    path = "/test"
    test_client.post("/_register", json={"path": path, "method": "GET", "response": expected_response_1})
    for _ in range(13):
        res = test_client.get(path)
        assert res.status_code == HTTP_200_OK
        assert res.json() == expected_response_1


def test_register_with_status_code(test_client):
    expected_response_1 = {"result": "success"}
    path = "/test"
    status_code = HTTP_201_CREATED
    test_client.post(
        "/_register",
        json={
            "path": path,
            "method": "GET",
            "count": 1,
            "response": expected_response_1,
            "status_code": status_code,
        },
    )
    res = test_client.get(path)
    assert res.status_code == status_code
    assert res.json() == expected_response_1


def test_register_with_different_methods(test_client):
    expected_response_1 = {"result": "success"}
    path = "/test"
    test_client.post(
        "/_register",
        json={
            "path": path,
            "method": "POST",
            "count": 1,
            "response": expected_response_1,
        },
    )
    res = test_client.get(path)
    assert res.status_code == HTTP_405_METHOD_NOT_ALLOWED
    res = test_client.post(path)
    assert res.status_code == HTTP_200_OK
    assert res.json() == expected_response_1


def test_register_multiple_paths(test_client):
    expected_response_1 = {"result": "success"}
    expected_response_2 = {"result": "success2"}
    path_1 = "/test"
    path_2 = "/test2"
    test_client.post("/_register", json={"path": path_1, "method": "GET", "count": 1, "response": expected_response_1})
    test_client.post("/_register", json={"path": path_2, "method": "GET", "count": 1, "response": expected_response_2})
    res = test_client.get(path_1)
    assert res.status_code == HTTP_200_OK
    assert res.json() == expected_response_1
    res = test_client.get(path_1)
    assert res.status_code == HTTP_404_NOT_FOUND
    res = test_client.get(path_2)
    assert res.status_code == HTTP_200_OK
    assert res.json() == expected_response_2
