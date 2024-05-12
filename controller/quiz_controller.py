from factory.controller_interface import ControllerInterface
from factory.database import Database
from flask import request, jsonify
from models.quiz import Quiz
from datetime import datetime
from bson.objectid import ObjectId
from bson.timestamp import Timestamp
import traceback


class QuizController(ControllerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.db = Database()
        self.collection_name = "quizzes"

    def find_all(self):
        try:
            fetched_documents = list(self.db.get_collection(self.collection_name).find())
            return jsonify([Quiz.to_object(quiz_doc).to_json() for quiz_doc in fetched_documents])
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def find_by_id(self, quiz_id):
        try:
            fetched_quiz = self.db.get_collection(self.collection_name).find_one({
                "_id": ObjectId(quiz_id)
            })
            if fetched_quiz is None:
                return {
                    "error": True,
                    "message": "Quiz not found",
                    "status": 404
                }

            return jsonify(Quiz.to_object(fetched_quiz).to_json())
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
            required_fields = ["title", "description", "total_questions", "passing_marks", "total_marks",
                               "questions_list", "created_by_user_id", "created_by_user_name"]
            for field in required_fields:
                if field not in request_json:
                    return {
                        "error": True,
                        "message": f"Missing required field: {field}",
                        "status": 400
                    }

            # Validate data types
            if not isinstance(request_json["total_questions"], int) or not isinstance(request_json["passing_marks"], int) or \
                    not isinstance(request_json["total_marks"], int):
                return {
                    "error": True,
                    "message": "Invalid data type for numeric fields",
                    "status": 400
                }

            # Validate questions_list format
            if not isinstance(request_json["questions_list"], list):
                return {
                    "error": True,
                    "message": "questions_list must be a list",
                    "status": 400
                }

            quiz = Quiz(
                title=request_json["title"],
                description=request_json["description"],
                total_questions=request_json["total_questions"],
                passing_marks=request_json["passing_marks"],
                total_marks=request_json["total_marks"],
                questions_list=request_json["questions_list"],
                created_by_user_id=request_json["created_by_user_id"],
                created_by_user_name=request_json["created_by_user_name"],
                quiz_open_date=None if "quiz_open_date" not in request_json else request_json["quiz_open_date"],
                last_attempt_date=None if "last_attempt_date" not in request_json else request_json["last_attempt_date"],
                quiz_status=request_json["quiz_status"],
            )

            inserted_document = self.db.create_one(self.collection_name, quiz.to_bson())
            if inserted_document is str:
                return inserted_document

            inserted_document["_id"] = str(inserted_document["_id"])
            inserted_document["quiz_open_date"] = inserted_document["quiz_open_date"].as_datetime() \
                if inserted_document["quiz_open_date"] else None
            inserted_document["last_attempt_date"] = inserted_document["last_attempt_date"].as_datetime() \
                if inserted_document["last_attempt_date"] else None
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
                    "message": "Quiz Id is not provided",
                    "error": True,
                    "status": 406
                }

            quiz_id_valid = self.db.get_collection(self.collection_name).count_documents({
                "_id": ObjectId(request_json["_id"])
            })
            if quiz_id_valid == 0:
                return {
                    "message": "Quiz Id is invalid",
                    "error": True,
                    "status": 406
                }

            # Validate data types
            if "total_questions" in request_json and not isinstance(request_json["total_questions"], int):
                return {
                    "error": True,
                    "message": "Invalid data type for total_questions",
                    "status": 400
                }
            if "passing_marks" in request_json and not isinstance(request_json["passing_marks"], int):
                return {
                    "error": True,
                    "message": "Invalid data type for passing_marks",
                    "status": 400
                }
            if "total_marks" in request_json and not isinstance(request_json["total_marks"], int):
                return {
                    "error": True,
                    "message": "Invalid data type for total_marks",
                    "status": 400
                }

            quiz: Quiz = Quiz.to_object(request_json)
            # Calculate total_marks and total_questions
            total_questions = len(request_json.get("questions_list", []))
            total_marks = sum(question.points for question in quiz.questions_list)

            quiz.total_questions = total_questions
            quiz.total_marks = total_marks
            quiz.updated_date = Timestamp(datetime.now(), 1)

            updated_document = self.db.update_one(self.collection_name, request_json["_id"], quiz.to_json())
            if updated_document is str:
                return updated_document

            return jsonify(Quiz.to_object(updated_document).to_json())
        except Exception as ex:
            traceback.print_exc()
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def delete_ele(self, quiz_id):
        try:
            delete_result = self.db.get_collection(self.collection_name).delete_one({
                "_id": ObjectId(quiz_id)
            })
            if delete_result.deleted_count == 0:
                return {
                    "error": True,
                    "message": "Quiz not found",
                    "status": 404
                }
            else:
                return {
                    "message": "Quiz deleted successfully",
                    "status": 200
                }
        except Exception as ex:
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }