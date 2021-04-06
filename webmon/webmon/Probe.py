import requests
import re

from abc import ABC, abstractmethod


class Probe(ABC):
    """
    This class is
    """

    def __init__(self, host: str, monitor_conf: dict):
        self.host = host
        self.monitor_conf = monitor_conf

    @abstractmethod
    def basic_probe(self):
        pass


class HTTPProbe(Probe):

    def basic_probe(self, req_timeout: int = 10) -> dict:
        """
        This method runs the basic probe and stores the result in a dictionary.

        :return: A dictionary with basic probe information
        """

        try:
            http_probe = requests.get(self.host, timeout=req_timeout)
            http_probe_response = {
                'return_code': http_probe.status_code,
                'response_time_sec': http_probe.elapsed.total_seconds(),
                'page_content': http_probe.text
            }
        except requests.exceptions.Timeout:
            http_probe_response = {
                'return_code': 0,
                'response_time_sec': float('Inf'),
                'page_content': ''
            }

        return http_probe_response

    def regex_probe(self, page_content: str, regex: str) -> bool:
        """
        This method runs a match regex into the page content. If the regex is
        found it returns True, otherwise it returns False.

        :param page_content: The page content to search for a regex match
        :param regex: The regex to match
        :return: True if there is a match, False otherwise
        """

        pattern = re.compile(regex)
        if pattern.findall(page_content):
            return True
        return False


class CreateProbe:
    """
    This class is used to build Monitor Objects. When adding new Appl Protocols
    another entry should be added to this class. Since the absence of a protocol
    implementation is an unrecoverable error a NotImplementedError is raised.
    """

    def get_probe(self, hostname: str, probe_details: dict,
                  probe_proto: str = 'HTTP'):

        if probe_proto == 'HTTP':
            return HTTPProbe(hostname, probe_details)
        else:
            raise NotImplementedError
