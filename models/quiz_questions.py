import os


class QuizQuestions:
    question_id: str | None
    question: str
    options: list[str]
    correct_option: int | str
    points: int

    def __init__(self, question, correct_option, points, options=None, question_id=None):
        self.question = question
        self.correct_option = correct_option
        self.points = points
        self.options = [] if options is None else options
        self.question_id = os.urandom(16).hex() if question_id is None else question_id

    def to_json(self):
        return {
            "question_id": self.question_id,
            "question": self.question,
            "options": self.options,
            "correct_option": self.correct_option,
            "points": self.points
        }

    def to_bson(self):
        return {
            "question_id": self.question_id,
            "question": self.question,
            "options": self.options,
            "correct_option": self.correct_option,
            "points": self.points
        }

    @staticmethod
    def to_object(bson_document):
        if isinstance(bson_document, QuizQuestions):
            return bson_document

        return QuizQuestions(
            question=bson_document["question"],
            options=bson_document["options"],
            correct_option=bson_document["correct_option"],
            points=bson_document["points"],
            question_id=bson_document.get("question_id") or None
        )
