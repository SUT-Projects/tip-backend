from factory.controller_interface import ControllerInterface
from factory.database import Database
from flask import request, jsonify
from models.user import User
from datetime import datetime
from hashlib import sha256
from bson.objectid import ObjectId
from bson.timestamp import Timestamp


class UserController(ControllerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.db = Database()
        self.collection_name = "users"

    def user_login(self):
        """
        Performs user login based on the provided email and password in the JSON request body.
        This method validates the user credentials against the specified collection.
        On successful login, it returns the user information.

        **Request Body:**
        - `email` (str): The user's email address. (Required)
        - `password` (str): The user's password. (Required)

        **Returns:**
        - On successful login: A JSON object containing:
            - `error`: False
            - `message`: "Login Successful"
            - `status`: 200
            - `user`: A JSON representation of the logged-in user object.
        - On invalid credentials: A JSON object containing:
            - `error`: False  (Consider using True for consistency)
            - `message`: "Invalid Credentials"
            - `status`: 401 (Unauthorized)
        - On suspended account: A JSON object containing:
            - `error`: False  (Consider using True for consistency)
            - `message`: "Login Failed: Account has been suspended"
            - `status`: 200
        - On deactivated account: A JSON object containing:
            - `error`: False  (Consider using True for consistency)
            - `message`: "Login Failed: Account has been deactivated"
            - `status`: 200
        - On error: A JSON object with error details, including:
            - `error`: True
            - `message`: A description of the error that occurred.
            - `status`: 500 (Internal Server Error)
        """
        try:
            request_json = request.get_json()
            password = sha256(request_json["password"].encode()).hexdigest()
            # Check for required fields in request body
            if "email" not in request_json or "password" not in request_json:
                return {
                    "error": True,
                    "message": "Missing required fields in request body",
                    "status": 400  # Bad Request
                }

            fetch_user = list(self.db.get_collection(self.collection_name).find({
                "email": request_json["email"],
                "password": password
            }).limit(1))
            if len(fetch_user) == 0:
                return {
                    "error": False,
                    "message": "Invalid Credentials",
                    "status": 401
                }
            user: User = User.to_object(fetch_user[0])
            if user.account_status == 2:
                return jsonify({
                    "error": True,
                    "message": "Login Failed: Account has been suspended",
                    "status": 200
                })

            if user.account_status == 3:
                return jsonify({
                    "error": True,
                    "message": "Login Failed: Account has been deactivated",
                    "status": 200
                })

            return jsonify({
                "error": False,
                "message": "Login Successful",
                "status": 200,
                "user": user.to_json()
            })
        except Exception as ex:
            print(ex)
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def find_all(self):
        """
        Retrieves all documents from the specified collection, sorted by the "name" field.

        This method fetches all documents from the collection and returns them as a list.
        The documents are sorted alphabetically by their "name" field before returning.

        **Returns:**
        - On success: A list of dictionaries representing the retrieved user documents, sorted by "name".
        - On error: A JSON object with error details, including:
            - `error`: A boolean flag indicating an error (True).
            - `message`: A description of the error that occurred.
            - `status`: An HTTP status code representing the error type (e.g., 500 for internal server error).

        **Raises:**
        - Exception: Any unexpected exceptions during the retrieval process.
        """

        try:
            fetched_documents = list(self.db.get_collection(self.collection_name).find())
            return jsonify([User.to_object(user_doc).to_json() for user_doc in fetched_documents])
        except Exception as ex:
            print(ex)
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def find_by_id(self, element_id):
        pass

    def create_ele(self):
        """
        Creates a new user document in the specified collection based on the provided JSON request.

        This method expects a JSON request body containing the user information.
        It validates for existing users with the same email address before creating a new document.

        **Request Body:**
        - `name` (str): The name of the user. (Required)
        - `email` (str): The unique email address of the user. (Required)
        - `password` (str): The user's password. (Required)
        - `userType` (int, optional): An integer representing the user type. Defaults to 0.
        - `department` (str, optional): The user's department.

        **Returns:**
        - On success: A JSON object containing the newly created user document with `_id` converted to a string.
        - On duplicate email error: A JSON object with a message indicating the email already exists.
            This response has an `error` flag set to `False` and an HTTP status code of 200.
        - On error: A JSON object with error details, including:
            - `message`: A description of the error that occurred.
            - `error`: A boolean flag indicating an error (True).
            - `status`: An HTTP status code representing the error type (e.g., 500 for internal server error).

        **Raises:**
        - Exception: Any unexpected exceptions during the creation process.
        """
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

            user: User = User(
                name=request_json["name"],
                email=request_json["email"],
                password=sha256(request_json["password"].encode()).hexdigest(),
                user_type=0 if request_json["userType"] is None else request_json["userType"],
                account_status=1,
                department=request_json["department"],
                created_date=Timestamp(datetime.now(), 1),
                updated_date=Timestamp(datetime.now(), 1)
            )

            inserted_document = self.db.create_one(self.collection_name, user.to_bson())
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
        """
        Updates a user document in the specified collection based on the provided ID from a JSON request.
        This method expects a JSON request body containing the updated user information.
        It validates the presence and validity of the user ID (`_id`) before proceeding.

        **Request Body:**
        - `_id` (str): The unique identifier of the user document to update. (Required)
        - Other fields (optional): Key-value pairs representing the updated user data.

        **Returns:**
        - On success: A JSON object containing the updated user document with `_id` converted to a string.
        - On error: A JSON object with error details, including:
            - `message`: A description of the error that occurred.
            - `error`: A boolean flag indicating an error (True).
            - `status`: An HTTP status code representing the error type (e.g., 400 for bad request,
            406 for not acceptable, 500 for internal server error).

        **Raises:**
        - Exception: Any unexpected exceptions during the update process.
        """
        try:
            request_json = request.get_json()
            if "_id" not in request_json or request_json["_id"] is None:
                return {
                    "message": "User Id is not provided",
                    "error": True,
                    "status": 406
                }

            user_id_valid = self.db.get_collection(self.collection_name).count_documents({
                "_id": ObjectId(request_json["_id"])
            })
            if user_id_valid == 0:
                return {
                    "message": "User Id is invalid",
                    "error": True,
                    "status": 406
                }

            request_json["created_date"] = Timestamp(datetime.strptime(request_json["created_date"], "%a, %d %b %Y %H:%M:%S %Z"), 1)
            request_json["updated_date"] = Timestamp(datetime.now(), 1)
            updated_document = self.db.update_one(self.collection_name, request_json["_id"], request_json)
            if updated_document is str:
                return updated_document

            updated_document["_id"] = str(updated_document["_id"])
            updated_document["created_date"] = updated_document["created_date"].as_datetime()
            updated_document["updated_date"] = updated_document["updated_date"].as_datetime()
            return jsonify(updated_document)
        except Exception as ex:
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }

    def delete_ele(self, user_id):
        try:
            print(user_id)
            delete_result = self.db.get_collection(self.collection_name).delete_one({
                "_id": ObjectId(user_id)
            })
            if delete_result.deleted_count == 0:
                return {
                    "error": True,
                    "message": "User not found",
                    "status": 404  # Not Found
                }

            return {
                "message": "User deleted successfully",
                "status": 200
            }
        except Exception as ex:
            return {
                "error": True,
                "message": str(ex),
                "status": 500
            }
