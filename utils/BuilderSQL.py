class SQLQuery:
    def __init__(self):
        self.query_type = None
        self.columns = None
        self.table = None
        self.joins = []
        self.conditions = []
        self.set_values = {}
        self.limit = None
        self.order_by = None

    def __str__(self) -> str:
        try:
            return self.Build()
        except ValueError:
            return "SELECT false"

    def Select(self, *columns):
        self.query_type = "SELECT"
        self.columns = ", ".join(columns)
        return self

    def Insert(self, table):
        self.query_type = "INSERT"
        self.table = table
        return self

    def Update(self, table):
        self.query_type = "UPDATE"
        self.table = table
        return self

    def Delete(self, table):
        self.query_type = "DELETE"
        self.table = table
        return self

    def From(self, table):
        self.table = table
        return self

    def Join(self, table, on_condition, join_type="INNER"):
        self.joins.append((join_type, table, on_condition))
        return self

    def Where(self, condition):
        self.conditions.append(condition)
        return self

    def Set(self, **values):
        self.set_values = values
        return self

    def Limit(self, limit):
        self.limit = limit
        return self

    def OrderBy(self, column, order="ASC"):
        self.order_by = f"{column} {order}"
        return self

    def Build(self):
        if self.query_type == "SELECT":
            query = f"SELECT {self.columns} FROM {self.table}"
        elif self.query_type == "INSERT":
            columns = ", ".join(self.set_values.keys())
            values = ", ".join(
                [
                    f"'{value}'" if isinstance(value, str) else str(value)
                    for value in self.set_values.values()
                ]
            )
            query = f"INSERT INTO {self.table} ({columns}) VALUES ({values})"
        elif self.query_type == "UPDATE":
            values = ", ".join(
                [f"{key}={self.set_values[key]}" for key in self.set_values.keys()]
            )
            query = f"UPDATE {self.table} SET {values}"
        elif self.query_type == "DELETE":
            query = f"DELETE FROM {self.table}"

        for join in self.joins:
            join_type, join_table, on_condition = join
            query += f" {join_type} JOIN {join_table} ON {on_condition}"

        if self.conditions:
            query += " WHERE " + " AND ".join(self.conditions)
        if self.order_by:
            query += f" ORDER BY {self.order_by}"
        if self.limit:
            query += f" LIMIT {self.limit}"

        try:
            return query
        except UnboundLocalError:
            raise ValueError("Empty query.")
