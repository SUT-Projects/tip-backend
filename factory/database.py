from pymongo import MongoClient
import config


class Database:
    def __init__(self, database_name="quiz_database") -> None:
        self.client = MongoClient(config.MONGODB_URI)
        self.db_instance = self.client[database_name]

    def find_all(self, collection_name):
        """
        Finds all elements from a specified collection.

        Args:
            collection_name: The name of the MongoDB collection to query.

        Returns:
            A list containing all elements from the specified collection.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """

        pass

    def find_by_id(self, collection_name, id):
        """
        Finds an element by its ID from a specified collection.

        Args:
            collection_name: The name of the MongoDB collection to query.
            id: The ID of the element to find.

        Returns:
            The element matching the provided ID, or None if not found.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """

        pass

    def create_one(self, collection_name, element):
        """
        Creates a new element in a specified collection.

        Args:
            collection_name: The name of the MongoDB collection to insert into.
            element: A dictionary representing the new element to create.

        Returns:
            The newly created element object.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        pass

    def update_one(self, collection_name, element_id, element):
        """
        Updates an existing element in a specified collection by its ID.

        Args:
            collection_name: The name of the MongoDB collection to update in.
            element_id: The ID of the element to update.
            element: A dictionary containing the updated data for the element.

        Returns:
            The updated element object.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """

        pass

    def delete_one(self, collection_name, element_id):
        """
        Deletes an element from a specified collection by its ID.

        Args:
            collection_name: The name of the MongoDB collection to delete from.
            element_id: The ID of the element to delete.

        Returns:
            None

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        
        pass
