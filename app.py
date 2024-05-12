from flask import Flask, request
from datetime import datetime
from models.movies import Movies
from controller.user_controller import UserController
from controller.quiz_controller import QuizController

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)
