from flask import Flask, jsonify
from datetime import datetime
from models.movies import Movies

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home_page():
    return {"message": "Hello world", "date": datetime.now()}


app.add_url_rule("/get-movies", view_func=Movies().get_movies, methods=["GET"])

if __name__ == "__main__":
    app.run(debug=True)
