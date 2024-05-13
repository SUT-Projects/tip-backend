from flask import Flask, request
from datetime import datetime
from models.movies import Movies
from controller.user_controller import UserController
from controller.quiz_controller import QuizController
from controller.forum_controller import ForumController
from controller.discussion_controller import DiscussionController
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET'])
def home_page():
    return {"message": "Hello world", "date": datetime.now()}


app.add_url_rule("/get-movies", view_func=Movies().get_movies, methods=["GET"])


@app.route("/user-login", methods=["POST"])
def user_login():
    return UserController().user_login()


@app.route("/get-all-users", methods=["GET"])
def get_all_users():
    return UserController().find_all()


@app.route("/create-user", methods=["POST"])
def create_user():
    return UserController().create_ele()


@app.route("/update-user", methods=["POST"])
def update_user():
    return UserController().update_ele()


@app.route("/delete-user", methods=["DELETE"])
def delete_user():
    user_id = request.args.get("user_id", default="").strip()
    if len(user_id) == 0:
        return {
            "error": True,
            "message": "Missing user ID",
            "status": 400  # Bad Request
        }

    print(request.args.get("user_id", default=""))
    return UserController().delete_ele(user_id)


@app.route("/get-all-quizzes", methods=["GET"])
def get_all_quizzes():
    return QuizController().find_all()


@app.route("/get-quiz", methods=["GET"])
def get_quiz():
    quiz_id = request.args.get("quiz_id", default="").strip()
    if len(quiz_id) == 0:
        return {
            "error": True,
            "message": "Missing quiz ID",
            "status": 400  # Bad Request
        }
    return QuizController().find_by_id(quiz_id)


@app.route("/create-quiz", methods=["POST"])
def create_quiz():
    return QuizController().create_ele()


@app.route("/update-quiz", methods=["POST"])
def update_quiz():
    return QuizController().update_ele()


@app.route("/delete-quiz", methods=["DELETE"])
def delete_quiz():
    quiz_id = request.args.get("quiz_id", default="").strip()
    if len(quiz_id) == 0:
        return {
            "error": True,
            "message": "Missing quiz ID",
            "status": 400  # Bad Request
        }
    return QuizController().delete_ele(quiz_id)


@app.route("/get-all-forums", methods=["GET"])
def get_all_forums():
    return ForumController().find_all()


@app.route("/get-forum", methods=["GET"])
def get_forum():
    forum_id = request.args.get("forum_id", default="").strip()
    if len(forum_id) == 0:
        return {
            "error": True,
            "message": "Missing forum ID",
            "status": 400  # Bad Request
        }
    return ForumController().find_by_id(forum_id)


@app.route("/create-forum", methods=["POST"])
def create_forum():
    return ForumController().create_ele()


@app.route("/update-forum", methods=["POST"])
def update_forum():
    return ForumController().update_ele()


@app.route("/get-forum-by-quiz", methods=["GET"])
def get_forum_by_quiz():
    quiz_id = request.args.get("quiz_id", default="").strip()
    if len(quiz_id) == 0:
        return {
            "error": True,
            "message": "Missing quiz ID",
            "status": 400  # Bad Request
        }
    return ForumController().get_forum_by_quiz(quiz_id)


@app.route("/get-forum-by-user", methods=["GET"])
def get_forum_by_user():
    user_id = request.args.get("user_id", default="").strip()
    if len(user_id) == 0:
        return {
            "error": True,
            "message": "Missing user ID",
            "status": 400  # Bad Request
        }
    return ForumController().get_forum_by_user(user_id)


@app.route("/delete-forum", methods=["DELETE"])
def delete_forum():
    forum_id = request.args.get("forum_id", default="").strip()
    if len(forum_id) == 0:
        return {
            "error": True,
            "message": "Missing forum ID",
            "status": 400  # Bad Request
        }
    return ForumController().delete_ele(forum_id)


@app.route("/get-all-discussions", methods=["GET"])
def get_all_discussion():
    forum_id = request.args.get("forum_id", default="").strip()
    if len(forum_id) == 0:
        return {
            "error": True,
            "message": "Missing forum ID",
            "status": 400  # Bad Request
        }
    return DiscussionController().find_by_forum(forum_id)


@app.route("/get-discussion", methods=["GET"])
def get_discussion():
    discussion_id = request.args.get("discussion_id", default="").strip()
    if len(discussion_id) == 0:
        return {
            "error": True,
            "message": "Missing discussion ID",
            "status": 400  # Bad Request
        }
    return DiscussionController().find_by_id(discussion_id)


@app.route("/create-discussion", methods=["POST"])
def create_discussion():
    return DiscussionController().create_ele()


@app.route("/update-discussion", methods=["POST"])
def update_discussion():
    return DiscussionController().update_ele()


@app.route("/delete-discussion", methods=["DELETE"])
def delete_discussion():
    discussion_id = request.args.get("discussion_id", default="").strip()
    if len(discussion_id) == 0:
        return {
            "error": True,
            "message": "Missing discussion ID",
            "status": 400  # Bad Request
        }
    return DiscussionController().delete_ele(discussion_id)


if __name__ == "__main__":
    app.run(debug=True)
