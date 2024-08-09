from typing import List, Union
from mysql.connector import Error
from database.Database import Database, CustomObject


class DatabaseOperation(Database):
    def __init__(self) -> None:
        super().__init__()

    def execute(
        self, query, return_as_object=False
    ) -> Union[List[CustomObject], List[tuple]]:
        try:
            if self.conn is None or not self.conn.is_connected():
                self._connect()

            cursor = self.conn.cursor(dictionary=return_as_object)
            cursor.execute(query)
            self.results = (
                [CustomObject(**row) for row in cursor.fetchall()]
                if return_as_object
                else cursor.fetchall()
            )
            self.info.update(
                {
                    "query": query,
                    "affected_rows": cursor.rowcount,
                    "status": "success",
                    "errors": None,
                    "has_changed": "not",
                }
            )
            if self.messages:
                print(self.info)
            return self.results

        except Error as e:
            self.info.update({"status": "error", "errors": str(e)})
            if self.messages:
                print(self.info)
            return None

    def execute_non_query(self, query) -> list:
        try:
            if self.conn is None or not self.conn.is_connected():
                self._connect()
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            self.info.update(
                {
                    "query": query,
                    "affected_rows": cursor.rowcount,
                    "status": "success",
                    "errors": None,
                    "has_changed": "yes",
                }
            )
            if self.messages:
                print(self.info)
            return self.info

        except Error as e:
            self.info.update({"status": "error", "errors": str(e)})
            if self.messages:
                print(self.info)
            return None

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeConnection()
