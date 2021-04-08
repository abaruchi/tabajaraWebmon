import unittest

from webstore import SQL


class TestProbe(unittest.TestCase):

    def setUp(self) -> None:
        self.test_table = "table_name"
        self.input_list = [('table1', 'val1'), ('table2', 'val2')]

        self.missing_table_list = [('', 'val1'), ('table2', 'val2')]
        self.missing_val_list = [('table1', ''), ('table2', 'val2')]
        self.wrong_val_list = []

        self.sql_generator = SQL.Command()

    def test_sql_insert_generator(self):

        self.assertEqual(
            self.sql_generator.insert(self.test_table, self.input_list),
            "INSERT INTO {} (table1, table2) VALUES ('val1', 'val2')".format(
                self.test_table))

    def test_sql_with_wrong_data(self):

        with self.assertRaises(AttributeError):
            self.sql_generator.insert(self.test_table, self.missing_table_list)

        with self.assertRaises(AttributeError):
            self.sql_generator.insert(self.test_table, self.missing_val_list)

        with self.assertRaises(AttributeError):
            self.sql_generator.insert(self.test_table, self.wrong_val_list)
