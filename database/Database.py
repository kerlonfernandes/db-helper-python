import mysql.connector
from mysql.connector import Error
from config.config import MYTEMPO_MYSQL_CONFIG

class CustomObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Database:
    def __init__(self, messages=False):
        self.host = MYTEMPO_MYSQL_CONFIG["host"]
        self.user = MYTEMPO_MYSQL_CONFIG["user"]
        self.password = MYTEMPO_MYSQL_CONFIG["password"]
        self.database = MYTEMPO_MYSQL_CONFIG["database"]
        self.messages = messages
        self.results = []
        self.info = {
            "status": "",
            "connection": "",
            "query": "",
            "affected_rows": "",
            "errors": "",
            "has_changed": "",
        }
        self.conn = None

    def _connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            if self.conn.is_connected():
                self.info["connection"] = "Connected"
                return True
            else:
                self.info["connection"] = "Failed to connect"
                return False
        except Error as e:
            self.info["connection"] = f"Error: {e}"
            return False

    def _disconnect(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            self.info["connection"] = "Disconnected"

    def executeQuery(self, query, return_as_object=False):
        if not self._connect():
            self.info["status"] = "error"
            self.info["errors"] = "Failed to connect to database"
            if self.messages:
                print(self.info)
            return None
        try:
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
        finally:
            self._disconnect()

    def executeNonQuery(self, query):
        if not self._connect():
            self.info["status"] = "error"
            self.info["errors"] = "Failed to connect to database"
            if self.messages:
                print(self.info)
            return None

        try:
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
        finally:
            self._disconnect()

    def closeConnection(self):
        try:
            self.conn.commit()
        except Exception as e:
            print(e)

        finally:
            self._disconnect()
            if self.messages:
                print(self.info)
