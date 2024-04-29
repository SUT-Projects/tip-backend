from abc import ABC, abstractmethod
from flask.views import MethodView


class ControllerInterface(ABC, MethodView):
    """
    This abstract class defines the interface for a data controller.

    The interface specifies methods for performing CRUD (Create, Read, Update, Delete) operations
    on a MongoDB collection. Subclasses implementing this interface should provide concrete
    implementations for these methods.
    """

    @abstractmethod
    def find_all(self):
        raise NotImplementedError("find() not implemented")

    @abstractmethod
    def find_by_id(self, element_id):
        raise NotImplementedError("find_by_id() not implemented")

    @abstractmethod
    def create_one(self):
        raise NotImplementedError("create_one() not implemented")

    @abstractmethod
    def update_one(self):
        raise NotImplementedError("update_one() not implemented")

    @abstractmethod
    def delete_one(self):
        raise NotImplementedError("delete_one() not implemented")
