import json
from flask import request
from database.models import Answers, Question, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, ValidationError, DoesNotExist
from resources.errors import SchemaValidationError, InternalServerError, UpdatingContentError


class AnswerUpvote(Resource):
    @jwt_required
    def put(self):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            args = request.args
            answer_id = args['answer_id']
            Answers.objects.get(id=answer_id).update(inc__vote=1)
            return {'Success': 'Answer is upvoted'}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingContentError
        except Exception as e:
            raise InternalServerError


class AnswerDownvote(Resource):
    @jwt_required
    def put(self):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            args = request.args
            answer_id = args['answer_id']
            Answers.objects.get(id=answer_id).update(inc__vote=-1)
            return {'Success': 'Answer is downvoted'}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingContentError
        except Exception as e:
            raise InternalServerError


class AnswerIsAccepted(Resource):
    @jwt_required
    def put(self):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            args = request.args
            answer_id = args['answer_id']
            question = Answers.objects.get(id=answer_id).to_json()
            question = json.loads(question)
            question_id = question['question']['$oid']
            question_user = Question.objects.get(id=question_id, added_by=user_id)
            Answers.objects.get(id=answer_id).update(is_accepted=True)
            return {'Success': 'Answer is accepted'}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingContentError
        except Exception as e:
            raise InternalServerError
