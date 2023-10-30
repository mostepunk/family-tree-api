from fastapi import status

from family.adapters.schemas.accounts import AccountSchema
from tests.fake_const import admin_answer


class TestLogin:
    async def token(self, client):
        response = await client.post(
            "/api/family/v1/accounts/login",
            data={"username": "admin", "password": "admin"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        answer = response.json()
        return answer.get("access_token")

    async def test_login(self, client):
        response = await client.post(
            "/api/family/v1/accounts/login",
            data={"username": "admin", "password": "admin"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        answer = response.json()
        self.token = answer.get("access_token")
        assert response.status_code == status.HTTP_200_OK

    async def test_login_failed(self, client):
        response = await client.post(
            "/api/family/v1/accounts/login",
            data={"username": "not_authorized", "password": "not_authorized"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_path_me(self, client):
        token = await self.token(client)

        response = await client.get(
            "/api/family/v1/accounts/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        admin = AccountSchema.parse_obj(response.json())
        assert admin == admin_answer

    async def test_return_token(self, client):
        token = await self.token(client)
        response = await client.get(
            "/api/family/v1/accounts/token",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == status.HTTP_200_OK
