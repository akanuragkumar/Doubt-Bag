from flask import Response, request
from database.models import Comments, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, InternalServerError, \
    UpdatingContentError, DeletingContentError, ContentNotExistsError, CreatingContentError


class CommentsApi(Resource):
    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            args = request.args
            question = args['question_id']
            comment = Comments(**body, question=question, added_by=user)
            comment.save()
            user.update(push__comments=comment)
            user.save()
            id = comment.id
            return {'Success': 'Your comment has been posted', 'id': str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except DoesNotExist:
            raise CreatingContentError
        except Exception as e:
            raise InternalServerError


class CommentApi(Resource):
    @jwt_required
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            comment = Comments.objects.get(id=id, added_by=user_id)
            body = request.get_json()
            Comments.objects.get(id=id).update(**body)
            return {'Success': 'Your comment has been updated'}, 200
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
            comment = Comments.objects.get(id=id, added_by=user_id)
            comment.delete()
            return {'Success': 'Your comment has been deleted'}, 200
        except DoesNotExist:
            raise DeletingContentError
        except Exception:
            raise InternalServerError

    def get(self, id):
        try:
            comments = Comments.objects.get(id=id).to_json()
            return Response(comments, mimetype="application/json", status=200)
        except DoesNotExist:
            raise ContentNotExistsError
        except Exception:
            raise InternalServerError
