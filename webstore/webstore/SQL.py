class Command(object):
    """
    This class is used to generate SQL commands. It must be the only place where
    SQL commands are defined and created. If new commands must be created, it
    must be added in this class.
    """

    def insert(self, table: str, values: list):
        """
        This method returns SQL insert commands. It avoids SQL Injection by
        (1) using positional arguments when creating the INSERT command and
        (2) it is used in main SQL writer by injection the main routine doesn't
        have direct access to this class.

        Reference: https://realpython.com/prevent-python-sql-injection/

        :param table: The table name where data will be inserted
        :param values: A list with tuples (column, value)
        :return: The insert command to add values into database
        """

        if not self.__list_validation(values):
            raise AttributeError

        sql_insert_cols = "("
        sql_insert_cols += ", ".join(map(lambda x: str(x[0]), values))
        sql_insert_cols += ")"

        sql_insert_val = "("
        sql_insert_val += ", ".join(map(lambda x: "\'{}\'".format(str(x[1])),
                                        values))
        sql_insert_val += ")"

        return "INSERT INTO {} {} VALUES {}".format(table, sql_insert_cols,
                                                    sql_insert_val)

    def __list_validation(self, values: list) -> bool:
        """
        This method is used to validate the list used as input to the SQL
        generator.

        :param values: A list with tuples (column, value)
        :return: True if the list is fine, False otherwise
        """

        if len(values) == 0:
            return False

        for value in values:
            col_name, value = value
            if len(col_name) == 0 or len(value) == 0:
                return False

        return True
