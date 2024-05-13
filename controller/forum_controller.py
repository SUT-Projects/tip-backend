from factory.controller_interface import ControllerInterface
from factory.database import Database
from flask import request, jsonify
from models.forum import Forum
from datetime import datetime
from bson.objectid import ObjectId
from bson.timestamp import Timestamp
from controller.discussion_controller import DiscussionController


class ForumController(ControllerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.db = Database()
        self.collection_name = "forums"

    def find_all(self):
        try:
            fetched_documents = list(self.db.get_collection(self.collection_name).find())
            return jsonify([Forum.to_object(forum_doc).to_json() for forum_doc in fetched_documents])
        except Exception as ex:
            print(ex)
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def find_by_id(self, forum_id):
        try:
            fetched_forum = self.db.get_collection(self.collection_name).find_one({
                "_id": ObjectId(forum_id)
            })
            if fetched_forum is None:
                return {
                    "error": True,
                    "message": "Forum not found",
                    "status": 404
                }

            return jsonify(Forum.to_object(fetched_forum).to_json())
        except Exception as ex:
            print(ex)
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def get_forum_by_quiz(self, quiz_id):
        try:
            if not self.db.check_id_existence("quizzes", quiz_id):
                return {
                    "error": True,
                    "message": "Quizz not found",
                    "status": 404
                }

            fetched_forums = list(self.db.get_collection(self.collection_name).find({
                "quiz_id": quiz_id
            }))

            return jsonify([Forum.to_object(f_doc).to_json() for f_doc in fetched_forums])
        except Exception as ex:
            print(ex)
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def get_forum_by_user(self, user_id):
        try:
            if not self.db.check_id_existence("users", user_id):
                return {
                    "error": True,
                    "message": "User not found",
                    "status": 404
                }

            fetched_forums = list(self.db.get_collection(self.collection_name).find({
                "created_by_user_id": user_id
            }))

            return jsonify([Forum.to_object(f_doc).to_json() for f_doc in fetched_forums])
        except Exception as ex:
            print(ex)
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def create_ele(self):
        try:
            request_json = request.get_json()

            # Validate required fields
            required_fields = ["title", "description", "created_by_user_id", "created_by_user_name"]
            for field in required_fields:
                if field not in request_json:
                    return {
                        "error": True,
                        "message": f"Missing required field: {field}",
                        "status": 400
                    }

            forum = Forum(
                title=request_json["title"],
                description=request_json["description"],
                created_by_user_id=request_json["created_by_user_id"],
                created_by_user_name=request_json["created_by_user_name"],
                quiz_id=request_json.get("quiz_id"),
                status=request_json.get("status", 1)
            )

            inserted_document = self.db.create_one(self.collection_name, forum.to_bson())
            if inserted_document is str:
                return inserted_document

            inserted_document["_id"] = str(inserted_document["_id"])
            inserted_document["created_date"] = inserted_document["created_date"].as_datetime()
            inserted_document["updated_date"] = inserted_document["updated_date"].as_datetime()

            return jsonify(inserted_document)
        except Exception as ex:
            print(ex)

            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def update_ele(self):
        try:
            request_json = request.get_json()
            if "_id" not in request_json or request_json["_id"] is None:
                return {
                    "message": "Forum Id is not provided",
                    "error": True,
                    "status": 406
                }

            forum_id_valid = self.db.get_collection(self.collection_name).count_documents({
                "_id": ObjectId(request_json["_id"])
            })
            if forum_id_valid == 0:
                return {
                    "message": "Forum Id is invalid",
                    "error": True,
                    "status": 406
                }

            forum: Forum = Forum.to_object(request_json)
            forum.updated_date = Timestamp(datetime.now(), 1)

            updated_document = self.db.update_one(self.collection_name, request_json["_id"], forum.to_json())
            if updated_document is str:
                return updated_document

            return jsonify(Forum.to_object(updated_document).to_json())
        except Exception as ex:
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def delete_ele(self, forum_id):
        try:
            discussion_delete_result = DiscussionController().delete_all_discussions(forum_id)
            if discussion_delete_result.get("error"):
                return discussion_delete_result

            delete_result = self.db.get_collection(self.collection_name).delete_one({
                "_id": ObjectId(forum_id)
            })
            if delete_result.deleted_count == 0:
                return {
                    "error": True,
                    "message": "Forum not found",
                    "status": 404
                }
            else:
                return {
                    "message": "Forum deleted successfully",
                    "status": 200
                }
        except Exception as ex:
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }
