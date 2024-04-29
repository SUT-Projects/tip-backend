from factory.database import Database
from flask import jsonify
from flask.views import MethodView
from bson import json_util


class Movies(MethodView):
    def __init__(self):
        self.db = Database("sample_mflix")
        self.collection_name = "movies"

    def get_movies(self):
        documents = self.db.db_instance.get_collection(self.collection_name).find().limit(10)
        movies = []
        for doc in documents:
            doc['_id'] = str(doc['_id'])
            movies.append(json_util.loads(json_util.dumps(doc)))

        return jsonify({
            "movies": movies
        })
