import unittest
import json

from tests.BaseCase import BaseCase


class TestGetQuestions(BaseCase):

    def test_empty_response(self):
        response = self.app.get('/api/questions')
        self.assertListEqual(response.json, []) 
        self.assertEqual(response.status_code, 200)

    def test_movie_response(self):
        # Given
        email = "akanuragkumar712@gmail.com"
        password = "mycoolpassword"
        user_payload = json.dumps({
            "email": email,
            "password": password
        })

        response = self.app.post('/api/auth/signup', headers={"Content-Type": "application/json"}, data=user_payload)
        user_id = response.json['id']
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
        response = self.app.post('/api/questions',
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {login_token}"},
                                 data=json.dumps(question_payload))

        # When
        response = self.app.get('/api/questions')
        added_movie = response.json[0]

        # Then
        self.assertEqual(question_payload['topics'], added_movie['topics'])
        self.assertEqual(question_payload['question_body'], added_movie['question_body'])
        self.assertEqual(question_payload['heading'], added_movie['heading'])
        self.assertEqual(user_id, added_movie['added_by']['$oid'])
        self.assertEqual(200, response.status_code)
