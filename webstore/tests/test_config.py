from webstore.webstore import Config
import unittest


class ConfigTest(unittest.TestCase):

    def setUp(self) -> None:

        self.missing_file = "file_that_doest_exist"
        self.conf_file = "config_test.json"

    def test_missing_config_file(self):

        with self.assertRaises(FileNotFoundError):
            conf = Config.UserConfig(self.missing_file)

    def test_config_file_ok(self):

        conf = Config.UserConfig(self.conf_file)

        self.assertEqual(
            conf.list_services(),
            ["KAFKA", "POSTGRESQL"])

        self.assertEqual(
            conf.get_service_details("POSTGRESQL"),
            {"uri": "postgres://some_postgresql_uri"}
        )
