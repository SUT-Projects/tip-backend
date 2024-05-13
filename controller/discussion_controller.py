from factory.controller_interface import ControllerInterface
from factory.database import Database
from flask import request, jsonify
from models.discussion import Discussion
from datetime import datetime
from bson.objectid import ObjectId
from bson.timestamp import Timestamp
import traceback


class DiscussionController(ControllerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.db = Database()
        self.collection_name = "discussions"

    def find_all(self):
        try:
            fetched_documents = list(self.db.get_collection(self.collection_name).find())
            return jsonify([Discussion.to_object(discussion_doc).to_json() for discussion_doc in fetched_documents])
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def find_by_id(self, discussion_id):
        try:
            fetched_discussion = self.db.get_collection(self.collection_name).find_one({
                "_id": ObjectId(discussion_id)
            })
            if fetched_discussion is None:
                return {
                    "error": True,
                    "message": "Discussion not found",
                    "status": 404
                }

            return jsonify(Discussion.to_object(fetched_discussion).to_json())
        except Exception as ex:
            print(ex)
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def find_by_forum(self, forum_id):
        try:
            if not self.db.check_id_existence("forums", forum_id):
                return {
                    "error": True,
                    "message": "Forum not found",
                    "status": 404
                }

            fetched_discussions = list(self.db.get_collection(self.collection_name).find({
                "forum_id": forum_id
            }))

            return jsonify([Discussion.to_object(f_doc).to_json() for f_doc in fetched_discussions])
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
            required_fields = ["title", "content", "created_by_user_id", "created_by_user_name", "forum_id"]
            for field in required_fields:
                if field not in request_json:
                    return {
                        "error": True,
                        "message": f"Missing required field: {field}",
                        "status": 400
                    }

            discussion = Discussion(
                title=request_json["title"],
                content=request_json["content"],
                created_by_user_id=request_json["created_by_user_id"],
                created_by_user_name=request_json["created_by_user_name"],
                forum_id=request_json["forum_id"],
                quiz_id=request_json.get("quiz_id"),
                status=request_json.get("status", 1)
            )

            inserted_document = self.db.create_one(self.collection_name, discussion.to_bson())
            if inserted_document is str:
                return inserted_document

            inserted_document["_id"] = str(inserted_document["_id"])
            inserted_document["created_date"] = inserted_document["created_date"].as_datetime()
            inserted_document["updated_date"] = inserted_document["updated_date"].as_datetime()

            return jsonify(inserted_document)
        except Exception as ex:
            print(ex)
            traceback.print_exc()
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
                    "message": "Discussion Id is not provided",
                    "error": True,
                    "status": 406
                }

            discussion_id_valid = self.db.get_collection(self.collection_name).count_documents({
                "_id": ObjectId(request_json["_id"])
            })
            if discussion_id_valid == 0:
                return {
                    "message": "Discussion Id is invalid",
                    "error": True,
                    "status": 406
                }

            discussion: Discussion = Discussion.to_object(request_json)
            discussion.updated_date = Timestamp(datetime.now(), 1)

            updated_document = self.db.update_one(self.collection_name, request_json["_id"], discussion.to_json())
            if updated_document is str:
                return updated_document

            return jsonify(Discussion.to_object(updated_document).to_json())
        except Exception as ex:
            traceback.print_exc()
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def delete_ele(self, discussion_id):
        try:
            delete_result = self.db.get_collection(self.collection_name).delete_one({
                "_id": ObjectId(discussion_id)
            })
            if delete_result.deleted_count == 0:
                return {
                    "error": True,
                    "message": "Discussion not found",
                    "status": 404
                }
            else:
                return {
                    "message": "Discussion deleted successfully",
                    "status": 200
                }
        except Exception as ex:
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def delete_all_discussions(self, forum_id):
        try:
            delete_result = self.db.get_collection(self.collection_name).delete_many({
                "forum_id": forum_id
            })
            return {
                "message": f"{delete_result.deleted_count} discussions deleted successfully",
                "status": 200
            }
        except Exception as ex:
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }
