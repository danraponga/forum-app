def validate_error(response, expected_status_code, expected_detail=None):
    assert response.status_code == expected_status_code
    if expected_detail:
        assert response.json()["detail"] == expected_detail
