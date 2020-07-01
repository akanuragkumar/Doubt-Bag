from mongoengine import CASCADE
from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash


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

