import unittest

from webmon import Output


class TestProbe(unittest.TestCase):

    def setUp(self) -> None:

        self.conf_missing_fields = {
                "AUTH":
                {
                    "ssl_cafile": "ca.pem",
                    "ssl_certfile": "service.cert"
                },
            "CONNECTION":
                {
                    "host": "",
                    "port": ""
                }
        }

    def test_invalid_aiven_conn(self):

        with self.assertRaises(ConnectionAbortedError):
            Output.ToKafka(self.conf_missing_fields)
