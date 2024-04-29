from flask import Flask, jsonify
from datetime import datetime
from db import MongoDBClient
from bson import json_util

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home_page():
    return {"message": "Hello world", "date": datetime.now()}


@app.route("/get-movies", methods=['GET'])
def get_movies():
    mongoClient = MongoDBClient()
    
    documents = mongoClient.get_collection('movies').find().limit(30)
    movies = []
    for doc in documents:
        doc['_id'] = str(doc['_id'])
        movies.append(json_util.loads(json_util.dumps(doc)))

    return jsonify({
        "movies": movies
    })


if __name__ == "__main__":
    app.run(debug=True)
