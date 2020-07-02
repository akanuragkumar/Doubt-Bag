import json

from tests.BaseCase import BaseCase


class TestUserLogin(BaseCase):
 
    def test_successful_login(self):
        # Given
        email = "akanuragkumar712@gmail.com"
        password = "mycoolpassword"
        user_payload = json.dumps({
            "email": email,
            "password": password
        })

        self.app.post('/api/auth/signup', headers={"Content-Type": "application/json"}, data=user_payload)
        response = self.app.post('/api/auth/login', headers={"Content-Type": "application/json"}, data=user_payload)
        login_token = response.json['token']

        question_payload = {
            "topics": [
                "general",
                "metal ability",
                "awareness"
            ],
            "question_body": "what is Doubt-bag 3?",
            "heading": "what is Doubt-bag 3?"
        }
        # When
        response = self.app.post('/api/questions',
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {login_token}"},
                                 data=json.dumps(question_payload))

        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)
