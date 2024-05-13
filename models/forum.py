from bson.timestamp import Timestamp
from datetime import datetime
from factory.helper import convert_to_timestamp


class Forum:
    _id: str | None
    title: str
    description: str
    created_by_user_id: str
    created_by_user_name: str
    quiz_id: str | None
    created_date: Timestamp
    updated_date: Timestamp
    status: int  # 0 -> inactive | 1 -> active

    def __init__(self, title, description, created_by_user_id, created_by_user_name, quiz_id=None,
                 _id=None,
                 created_date=Timestamp(datetime.now(), 1),
                 updated_date=Timestamp(datetime.now(), 1),
                 status=1
                 ):
        self.quiz_id = quiz_id if quiz_id else None
        self._id = _id
        self.title = title
        self.description = description
        self.created_by_user_name = created_by_user_name
        self.created_by_user_id = created_by_user_id
        self.created_date = convert_to_timestamp(created_date)
        self.updated_date = convert_to_timestamp(updated_date)
        self.status = status

    def to_json(self):
        return {
            "_id": None if self._id is None else str(self._id),
            "title": self.title,
            "description": self.description,
            "created_by_user_id": self.created_by_user_id,
            "created_by_user_name": self.created_by_user_name,
            "quiz_id": self.quiz_id,
            "created_date": self.created_date.as_datetime(),
            "updated_date": self.updated_date.as_datetime(),
            "status": self.status
        }

    def to_bson(self):
        return {
            "_id": None if self._id is None else self._id,
            "title": self.title,
            "description": self.description,
            "created_by_user_id": self.created_by_user_id,
            "created_by_user_name": self.created_by_user_name,
            "quiz_id": self.quiz_id,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
            "status": self.status
        }

    @staticmethod
    def to_object(bson_document):
        if isinstance(bson_document, Forum):
            return bson_document

        return Forum(
            _id=bson_document["_id"],
            title=bson_document["title"],
            description=bson_document["description"],
            created_by_user_id=bson_document["created_by_user_id"],
            created_by_user_name=bson_document["created_by_user_name"],
            quiz_id=bson_document["quiz_id"],
            created_date=bson_document["created_date"],
            updated_date=bson_document["updated_date"],
            status=bson_document["status"]
        )