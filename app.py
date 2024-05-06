from flask import Flask
from datetime import datetime
from models.movies import Movies
from models.user import User

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home_page():
    return {"message": "Hello world", "date": datetime.now()}


app.add_url_rule("/get-movies", view_func=Movies().get_movies, methods=["GET"])
app.add_url_rule("/create-new-user", view_func=User().create_one, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)
