# Doubt-Bag
This app provides a platform for users to ask doubts, tag those questions to multiple topics and in turn, other users can comment on that question for further clarification and if they think they know the solution, they can answer the question. Further, if someone has doubts regarding the solution, people can post a comment for that solution. Lastly, if people are satisfied or dissatisfied with the solution, They can upvote or downvote the solution. The author of the question if he/she finds the answer satisfactory they can accept the answer.

You can read more about doubt-bag app and tutorial in [medium-article](https://medium.com/@akanuragkumar712/building-flask-rest-app-with-flask-restful-auth-mongodb-7412bdef5d1e).

## Quickstart

To work in a sandboxed Python environment it is recommended to install the app in a Python [virtualenv](https://pypi.python.org/pypi/virtualenv).

1. Install dependencies

    ```bash
    $ cd /path/to/Doubt-Bag
    $ pip install -r requirements.txt
    ```
2. .env FILE contains environment variable for MongoDB, JWT, and mail- server. Export this file to use this an environment variable for our app.

    ```bash
    $ export ENV_FILE_LOCATION=./.env
    ```
3. Start SMTP server in the terminal with:

    ```bash
    $ python -m smtpd -n -c DebuggingServer localhost:1025
    ```
   This will create an SMTP server for testing our email feature.

4. Run server

   ```bash
   $ python run.py
   ```

   View app at http://127.0.0.1:5000/<endpoints>
  
5. Run the Test-cases:
    Before running our first test make sure to export the environment variable ENV_FILE_LOCATION with the location to the test env file.

    ```bash
    $ export ENV_FILE_LOCATION=./.env.test
    # for running single unit test case
    $ python -m unittest tests/test_signup.py
    # running all unit test cases together
    $ python -m unittest --buffer
    ```
   ## Tech-stack used for Doubt bag:
      1. Flask — For our web server.
      2. flask-restful — For building cool Rest-APIs.
      3. virtualenv For managing python virtual environments.
      4. mongoengine — For managing our database.
      5. flask-marshmallow — For serializing user requests.
      6. Postman — For testing our APIs
      7. Flask-Bcrypt For hashing user password.
      8. Flask-JWT-Extended For creating tokens for authorization and authentication. 
   ## Project Structure


```shell
Doubt-Bag/                        
├── databases
│   ├── db.py
│   └── models.py
├── resources
│   ├── answer.py
│   ├── auth.py
│   ├── comment.py
│   ├── comment_answer.py
│   ├── errors.py
│   ├── question.py
│   ├── reset_password.py
│   ├── routes.py
│   └── votes.py
├── tests
│   ├── __init__.py
│   ├── Basecase.py
│   ├── test_create_question.py
│   ├── test_get_questions.py
│   ├── test_login.py
│   └── test_signup.py
├── templates/email
│   ├── reset_password.html
│   └── reset+password.txt
│   
├── services
│   └── mail_service.py
├── .env
├── .env.test
├── app.py
├── requirements.txt
└── run.py
   
```   
      
  ## Database Schema:
     ```shell
    class Question(db.Document):
    heading = db.StringField(required=True, unique=True)
    topics = db.ListField(db.StringField(), required=True)
    question_body = db.StringField(required=True)
    added_by = db.ReferenceField('User')


    class Comments(db.Document):
        comment = db.StringField(required=True)
        question = db.ReferenceField('Question', reverse_delete_rule=CASCADE)
        added_by = db.ReferenceField('User')


    class Answers(db.Document):
        answer = db.StringField(required=True)
        vote = db.IntField()
        is_accepted = db.BooleanField(default=False)
        question = db.ReferenceField('Question')
        added_by = db.ReferenceField('User')


    class AnswerComments(db.Document):
        comment = db.StringField(required=True)
        answer = db.ReferenceField('Answers', reverse_delete_rule=CASCADE)
        added_by = db.ReferenceField('User')


    class User(db.Document):
        email = db.EmailField(required=True, unique=True)
        password = db.StringField(required=True, min_length=6)
        questions = db.ListField(db.ReferenceField('Question', reverse_delete_rule=db.PULL))
        comments = db.ListField(db.ReferenceField('Comments', reverse_delete_rule=db.PULL))
        answers = db.ListField(db.ReferenceField('Answers', reverse_delete_rule=db.PULL))
        answers_comment = db.ListField(db.ReferenceField('AnswerComments', reverse_delete_rule=db.PULL))

        def hash_password(self):
            self.password = generate_password_hash(self.password).decode('utf8')

        def check_password(self, password):
            return check_password_hash(self.password, password)


    User.register_delete_rule(Question, 'added_by', db.CASCADE)
    User.register_delete_rule(Comments, 'added_by', db.CASCADE)
    User.register_delete_rule(Answers, 'added_by', db.CASCADE)
    User.register_delete_rule(AnswerComments, 'added_by', db.CASCADE)
    ```
  ## Api Endpoints:
  ### Auth
1. `POST /api/auth/signup` 

```json
 application/json - [{"email": "akanuragkumar712@gmail.com","password": "itssocool"}]
```
##### `response`

```json
 {"Success": "You successfully signed up!","id": <object_id>}
```
2. `POST /api/auth/login` 

```json
 application/json - [{"email": "akanuragkumar712@gmail.com","password": "itssocool"}]
```
##### `response`

```json
 {"token": <token>}
```
3. `POST /api/auth/forget` 

```json
 application/json - [{"email": "akanuragkumar712@gmail.com"]
```
##### `response`

```json
 a mail will be send with reset password token
```
4. `POST /api/auth/reset` 

```json
 application/json - [{"reset_token": <reset_token>,"password": "thisisalsocool"]
```
##### `response`

```json
 new password is set for the account and now the user has to login again.
```
### Question
1. `POST /api/question` 

```json
 application/json - [{"topics": ["general","metal ability","awareness"],"question_body": "what is Doubt-bag 3?","heading": "what is Doubt-bag 3?"}]
```
##### `response`

```json
{"Success": "Your question has been posted","id": <object_id>}
```
2. `GET /api/question/<id>` 

##### `response`

```json
 {"question": [{"_id": {"$oid": <object_id>}, "heading": "what is Doubt-bag?", "topics": ["general", "metal ability", "awareness"], "question_body": "what is Doubt-bag?", "added_by": {"$oid": <object_id>}}], "comments": [{"_id": {"$oid": <object_id>"}, "comment": "This is a very good question", "question": {"$oid": <object_id>}, "added_by": {"$oid": <object_id>}}, {"_id": {"$oid": <object_id>}, "comment": "This is a very good question-1(duplicate)", "question": {"$oid": <object_id>}, "added_by": {"$oid": <object_id>}}], "answers": [{"_id": {"$oid": <object_id>}, "answer": "This is a store house of all doubts people can have ranging to different topic.", "question": {"$oid": <object_id>}, "added_by": {"$oid": <object_id>}}, {"_id": {"$oid": <object_id>}, "answer": "This is a store house of all doubts people can have ranging to different topic.(duplicate)", "question": {"$oid": <object_id>}, "added_by": {"$oid": <object_id>}}]}
```
3. `PUT /api/question/<id>` 

```json
 application/json - [{"topics": ["science","metal ability","awareness"],"question_body": "what is Doubt-bag 3?","heading": "what is Doubt-bag 3?"}]
```
##### `response`

```json
 {"Success": "Your question has been updated"}
```
4. `DELETE /api/question/<id>` 

##### `response`

```json
 {"Success": "Your question has been deleted"}
```
### Comments
1. `POST /api/comments?question_id=<id>` 

```json
 application/json - [{"comment" : "This is a very good question-1(duplicate)"}]
```
##### `response`

```json
{"Success": "Your comment has been posted","id": <object_id>}
```
2. `GET /api/comment/<id>` 

##### `response`

```json
 [{"comment" : "This is a very good question-1(duplicate)", "question": {"$oid": <object_id>}, "added_by": {"$oid": <object_id>}]
```
3. `PUT /api/comments/<id>` 

```json
application/json - [{"comment" : "This is a very good question-1"}]
```
##### `response`

```json
{"Success": "Your comment has been updated"}
```
4. `DELETE /api/comments/<id>` 

##### `response`

```json
 {"Success": "Your comment has been deleted"}
```
### Answers
1. `POST /api/answers?question_id=<id>` 

```json
 application/json - [{"answer" : "This is a very good question-1(duplicate)"}]
```
##### `response`

```json
{"Success": "Your answer has been posted","id": <object_id>}
```
2. `GET /api/answers/<id>` 

##### `response`

```json
 [{"answer" : "This is a very good question-1(duplicate)", "question": {"$oid": <object_id>}, "added_by": {"$oid": <object_id>},{"answer_comment" : "This is a very good question-1","added_by": {"$oid": <object_id>}]
```
3. `PUT /api/answers/<id>` 

```json
application/json - [{"answer" : "This is a very good question-1"}]
```
##### `response`

```json
{"Success": "Your answer has been updated"}
```
4. `DELETE /api/answer/<id>` 

##### `response`

```json
 {"Success": "Your answer has been deleted"}
```
### Answer_comment
1. `POST /api/answer_comment?answer_id=<id>` 

```json
 application/json - [{"answer_comment" : "This is a very good question-1(duplicate)"}]
```
##### `response`

```json
{"Success": "Your comment has been posted","id": <object_id>}
```
2. `GET /api/answer_comment/<id>` 

##### `response`

```json
 [{"comment" : "This is a very good question-1(duplicate)", "question": {"$oid": <object_id>}, "added_by": {"$oid": <object_id>}]
```
3. `PUT /api/answer_comment/<id>` 

```json
application/json - [{"answer_comment" : "This is a very good question-1"}]
```
##### `response`

```json
{"Success": "Your comment has been updated"}
```
4. `DELETE /api/answer_comment/<id>` 

##### `response`

```json
{"Success": "Your comment has been deleted"}
```
### Vote and Accept of Answer
1. `PUT /api/upvote?answer_id=<id>` 

##### `response`

```json
{'Success': 'Answer is upvoted'}
```
2. `PUT /api/downvote?answer_id=<id>` 

##### `response`

```json
{'Success': 'Answer is downvoted'}
```
3. `PUT /api/accepted?answer_id=<id>` 

##### `response`

```json
{'Success': 'Answer is accepted'}
```
