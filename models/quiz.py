from datetime import datetime
from bson.timestamp import Timestamp
from bson.objectid import ObjectId
from models.quiz_questions import QuizQuestions
from factory.helper import convert_to_timestamp


class Quiz:
    _id: ObjectId | str | None
    title: str
    description: str
    questions_list: list[QuizQuestions]
    total_questions: int
    passing_marks: int
    total_marks: int
    created_by_user_id: str
    created_by_user_name: str
    quiz_open_date: Timestamp
    last_attempt_date: Timestamp
    quiz_status: int
    created_date: Timestamp
    updated_date: Timestamp

    def __init__(self, title, description, total_questions, passing_marks, total_marks,
                 created_by_user_id, created_by_user_name, questions_list: list[QuizQuestions] = None, quiz_open_date=None, last_attempt_date=None,
                 quiz_status=1,
                 _id=None,
                 created_date=Timestamp(datetime.now(), 1),
                 updated_date=Timestamp(datetime.now(), 1)
                 ):

        if questions_list is None:
            questions_list = []

        self._id = _id
        self.title = title
        self.description = description
        self.quiz_status = quiz_status
        self.total_questions = total_questions
        self.passing_marks = passing_marks
        self.total_marks = total_marks
        self.questions_list = [QuizQuestions.to_object(ques) for ques in list(questions_list)]
        self.created_by_user_id = created_by_user_id
        self.created_by_user_name = created_by_user_name
        self.quiz_open_date = convert_to_timestamp(quiz_open_date)
        self.last_attempt_date = convert_to_timestamp(last_attempt_date)
        self.created_date = convert_to_timestamp(created_date)
        self.updated_date = convert_to_timestamp(updated_date)

    def to_json(self):
        return {
            "_id": None if self._id is None else str(self._id),
            "title": self.title,
            "description": self.description,
            "total_questions": self.total_questions,
            "passing_marks": self.passing_marks,
            "total_marks": self.total_marks,
            "questions_list": [question.to_json() for question in self.questions_list],
            "created_by_user_id": self.created_by_user_id,
            "created_by_user_name": self.created_by_user_name,
            "quiz_open_date": self.quiz_open_date.as_datetime() if self.quiz_open_date else None,
            "last_attempt_date": self.last_attempt_date.as_datetime() if self.last_attempt_date else None,
            "quiz_status": self.quiz_status,
            "created_date": self.created_date.as_datetime(),
            "updated_date": self.updated_date.as_datetime()
        }

    def to_bson(self):
        return {
            "_id": None if self._id is None else self._id,
            "title": self.title,
            "description": self.description,
            "total_questions": self.total_questions,
            "passing_marks": self.passing_marks,
            "total_marks": self.total_marks,
            "questions_list": [question.to_bson() for question in self.questions_list],
            "created_by_user_id": self.created_by_user_id,
            "created_by_user_name": self.created_by_user_name,
            "quiz_open_date": self.quiz_open_date if self.quiz_open_date else None,
            "last_attempt_date": self.last_attempt_date if self.last_attempt_date else None,
            "quiz_status": self.quiz_status,
            "created_date": self.created_date,
            "updated_date": self.updated_date
        }

    @staticmethod
    def to_object(bson_document):
        return Quiz(
            _id=None if bson_document["_id"] is None else str(bson_document["_id"]),
            title=bson_document["title"],
            description=bson_document["description"],
            total_questions=bson_document["total_questions"],
            passing_marks=bson_document["passing_marks"],
            total_marks=bson_document["total_marks"],
            questions_list=[QuizQuestions(
                question=ques_doc["question"],
                options=[str(op) for op in list(ques_doc["options"])],
                correct_option=ques_doc["correct_option"],
                points=ques_doc["points"],
                question_id=ques_doc["question_id"]
            ) for ques_doc in list(bson_document["questions_list"])],
            created_by_user_id=bson_document["created_by_user_id"],
            created_by_user_name=bson_document["created_by_user_name"],
            quiz_open_date=bson_document["quiz_open_date"] if bson_document["quiz_open_date"] else None,
            last_attempt_date=bson_document["last_attempt_date"] if bson_document["last_attempt_date"] else None,
            quiz_status=bson_document["quiz_status"],
            created_date=bson_document["created_date"],
            updated_date=bson_document["updated_date"]
        )

