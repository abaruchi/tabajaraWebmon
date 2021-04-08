import unittest

import requests
import requests_mock

from webmon import Config, Probe


class TestProbe(unittest.TestCase):

    def setUp(self) -> None:
        self.conf = Config.UserConfig(config_path='test/config_test.json')
        self.probe = Probe.CreateProbes()

        self.text_url_01 = \
            "Lorem ipsum dolor sit amet - pattern01 and Pattern02"

    def test_basic_and_regex_probe(self):
        mocked_url = 'https://mock_url_01/'
        with requests_mock.Mocker() as mock:
            mock.get(mocked_url,
                     text=self.text_url_01, status_code=200)
            probe_test = self.probe.get_probe(mocked_url,
                                              self.conf.get_mon_details(mocked_url),
                                              self.conf.get_mon_details(mocked_url)['PROTO'])
            # Basic Probe Test
            self.assertEqual(
                probe_test.basic_probe()['return_code'], 200)
            self.assertEqual(
                probe_test.basic_probe()['page_content'], self.text_url_01)

            # Regex Probe Test
            for idx, regex in enumerate(
                    self.conf.get_mon_details(mocked_url)['REGEX_MON']):
                if idx == 2:
                    self.assertFalse(
                        probe_test.regex_probe(
                            probe_test.basic_probe()['page_content'], regex)
                    )
                else:
                    self.assertTrue(
                        probe_test.regex_probe(
                            probe_test.basic_probe()['page_content'], regex)
                    )

    def test_no_protocol_implementation(self):
        mocked_url = 'https://mock_url_03/'
        with self.assertRaises(NotImplementedError):
            self.probe.get_probe(
                mocked_url,
                self.conf.get_mon_details(mocked_url),
                probe_proto=self.conf.get_mon_details(mocked_url)['PROTO'])

    def test_timeout_probe(self):
        mocked_url = 'https://mock_url_02/'
        with requests_mock.Mocker() as mock:
            mock.get(mocked_url, exc=requests.exceptions.Timeout)
            probe_test = self.probe.get_probe(mocked_url,
                                              self.conf.get_mon_details(mocked_url),
                                              self.conf.get_mon_details(mocked_url)['PROTO'])

            # Basic Probe Test
            self.assertEqual(
                probe_test.basic_probe()['return_code'], 0)
            self.assertEqual(
                probe_test.basic_probe()['page_content'], '')
            self.assertEqual(
                probe_test.basic_probe()['response_time_sec'], float('Inf'))
