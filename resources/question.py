import json
from flask import Response, request
from database.models import Question, Comments, Answers, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, InternalServerError, \
    UpdatingContentError, DeletingContentError, ContentNotExistsError, CreatingContentError


class QuestionsApi(Resource):
    def get(self):
        query = Question.objects()
        questions = Question.objects().to_json()
        return Response(questions, mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            question = Question(**body, added_by=user)
            question.save()
            user.update(push__questions=question)
            user.save()
            id = question.id
            return {'Success': 'Your question has been posted', 'id': str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except DoesNotExist:
            raise CreatingContentError
        except Exception as e:
            raise InternalServerError


class QuestionApi(Resource):
    @jwt_required
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            question = Question.objects.get(id=id, added_by=user_id)
            body = request.get_json()
            Question.objects.get(id=id).update(**body)
            return {'Success': 'Your question has been updated'}, 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingContentError
        except Exception:
            raise InternalServerError

    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            if Answers.objects.get(question=id):
                return {'error': 'You cannot delete this question as it has an solution'}, 400
            else:
                question = Question.objects.get(id=id, added_by=user_id)
                question.delete()
            return {'Success': 'Your question has been deleted'}, 200
        except DoesNotExist:
            raise DeletingContentError
        except Exception:
            raise InternalServerError

    def get(self, id):
        try:
            content = {'question': json.loads(Question.objects.filter(id=id).to_json()),
                       'comments': json.loads(Comments.objects.filter(question=id).to_json()),
                       'answers': json.loads(Answers.objects.filter(question=id).to_json())}
            return content
        except DoesNotExist:
            raise ContentNotExistsError
        except Exception:
            raise InternalServerError
