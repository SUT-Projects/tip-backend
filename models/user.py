from factory.controller_interface import ControllerInterface
from factory.database import Database
from flask import request, jsonify


class User(ControllerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.db = Database()
        self.collection_name = "users"

    def user_login(self):
        pass

    def find_all(self):
        pass

    def find_by_id(self, element_id):
        pass

    def create_one(self):
        try:
            request_json = request.get_json()
            fetched_document = self.db.get_collection(self.collection_name).find_one({
                "email": request_json["email"]
            })

            if fetched_document is not None:
                return {
                    "message": f"user already exists with {request_json['email']}. Please use different email address",
                    "status": 200,
                    "error": False,
                }

            return jsonify({})
        except Exception as ex:
            print(ex)
            return "error"

    def update_one(self):
        pass

    def delete_one(self):
        pass
