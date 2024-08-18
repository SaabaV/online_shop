from fastapi.testclient import TestClient
from fastapi import Depends
from user_authorization.auth import get_current_user, User, oauth2_scheme
from user_authorization.token import create_access_token
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

class AuthTests(TestClient):
    def setUp(self):
        self.client = TestClient(app)
        self.user_data = {"user_id": "123"}
        self.token = create_access_token(self.user_data)
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def test_get_current_user_valid_token(self):
        response = self.client.get("/users/me", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"username": "123"})

    def test_get_current_user_invalid_token(self):
        response = self.client.get("/users/me", headers={"Authorization": "Bearer invalidtoken"})
        self.assertEqual(response.status_code, 401)
