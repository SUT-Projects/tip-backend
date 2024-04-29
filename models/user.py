from factory.controller_interface import ControllerInterface
from factory.database import Database


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
        pass

    def update_one(self):
        pass

    def delete_one(self):
        pass
