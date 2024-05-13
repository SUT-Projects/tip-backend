from bson.timestamp import Timestamp
from datetime import datetime
from factory.helper import convert_to_timestamp


class Discussion:
    def __init__(self, title, content, created_by_user_id, created_by_user_name, forum_id, quiz_id=None, _id=None,
                 created_date=Timestamp(datetime.now(), 1), updated_date=Timestamp(datetime.now(), 1),
                 status=1):
        self._id = _id
        self.title = title
        self.content = content
        self.created_by_user_id = created_by_user_id
        self.created_by_user_name = created_by_user_name
        self.forum_id = forum_id
        self.quiz_id = None if quiz_id is None else quiz_id
        self.created_date = convert_to_timestamp(created_date)
        self.updated_date = convert_to_timestamp(updated_date)
        self.status = status

    def to_json(self):
        return {
            "_id": None if self._id is None else str(self._id),
            "title": self.title,
            "content": self.content,
            "created_by_user_id": self.created_by_user_id,
            "created_by_user_name": self.created_by_user_name,
            "forum_id": self.forum_id,
            "quiz_id": self.quiz_id,
            "created_date": self.created_date.as_datetime(),
            "updated_date": self.updated_date.as_datetime(),
            "status": self.status
        }

    def to_bson(self):
        return {
            "_id": None if self._id is None else self._id,
            "title": self.title,
            "content": self.content,
            "created_by_user_id": self.created_by_user_id,
            "created_by_user_name": self.created_by_user_name,
            "forum_id": self.forum_id,
            "quiz_id": self.quiz_id,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
            "status": self.status
        }

    @staticmethod
    def to_object(bson_document):
        if isinstance(bson_document, Discussion):
            return bson_document

        return Discussion(
            _id=bson_document["_id"],
            title=bson_document["title"],
            content=bson_document["content"],
            created_by_user_id=bson_document["created_by_user_id"],
            created_by_user_name=bson_document["created_by_user_name"],
            forum_id=bson_document["forum_id"],
            quiz_id=bson_document["quiz_id"],
            created_date=bson_document["created_date"],
            updated_date=bson_document["updated_date"],
            status=bson_document["status"]
        )
