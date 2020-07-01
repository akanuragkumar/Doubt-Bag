from resources.question import QuestionsApi, QuestionApi
from resources.comment import CommentsApi, CommentApi
from resources.answer import AnswersApi, AnswerApi
from resources.vote import AnswerUpvote, AnswerDownvote, AnswerIsAccepted
from resources.comment_answer import AnswerCommentsApi, AnswerCommentApi
from resources.auth import SignupApi, LoginApi
from resources.reset_password import ForgotPassword, ResetPassword


def initialize_routes(api):
    api.add_resource(QuestionsApi, '/api/questions')
    api.add_resource(QuestionApi, '/api/questions/<id>')

    api.add_resource(CommentsApi, '/api/comments')
    api.add_resource(CommentApi, '/api/comments/<id>')

    api.add_resource(AnswersApi, '/api/answers')
    api.add_resource(AnswerApi, '/api/answers/<id>')

    api.add_resource(AnswerCommentsApi, '/api/answer-comments')
    api.add_resource(AnswerCommentApi, '/api/answer-comments/<id>')

    api.add_resource(AnswerUpvote, '/api/upvote')
    api.add_resource(AnswerDownvote, '/api/downvote')
    api.add_resource(AnswerIsAccepted, '/api/accepted')

    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')

    api.add_resource(ForgotPassword, '/api/auth/forgot')
    api.add_resource(ResetPassword, '/api/auth/reset')
