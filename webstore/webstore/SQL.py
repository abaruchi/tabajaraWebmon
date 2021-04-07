

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

        :param table: The table name to
        :param values: A list with tuples (column, value)
        :return: The insert command to add values into database
        """

        sql_insert_cols = "("
        sql_insert_cols += ", ".join(map(lambda x: str(x[0]), values))
        sql_insert_cols += ")"

        sql_insert_val = "("
        sql_insert_val += ", ".join(map(lambda x: str(x[1]), values))
        sql_insert_val += ")"

        return "INSERT INTO {} {} VALUES {}".format(table, sql_insert_cols,
                                                    sql_insert_val)
