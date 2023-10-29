from fastapi import status


def test_get_all_statuses(client):
    response = client.get("/api/family/v1/accounts/login")

    assert response.status_code == status.HTTP_200_OK
