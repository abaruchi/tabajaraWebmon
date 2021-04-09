import requests
import re
from datetime import datetime

from abc import ABC, abstractmethod

"""
Design Patterns example that I usually look when implementing:
https://refactoring.guru/design-patterns/python
"""


class Probe(ABC):
    """
    This abstract class must be used to implement probes in different
    applications protocols.
    """

    def __init__(self, host: str, monitor_conf: dict):
        self.host = host
        self.monitor_conf = monitor_conf

    @abstractmethod
    def basic_probe(self) -> dict:
        """
        Implements basic probe mechanisms for a given protocol.

        :return: A dictionary with probed data from a host.
        """
        pass

    def get_hostname(self):
        return self.host

    def get_monitor_details(self):
        return self.monitor_conf


class HTTPProbe(Probe):

    def basic_probe(self, req_timeout: int = 10) -> dict:
        """
        This method runs the basic probe to HTTP Protocol using requests
        library.

        :param req_timeout: Max waiting time (in seconds) to probe the Host
        :return: A dictionary with basic probe information
        """

        try:
            http_probe = requests.get(self.host, timeout=req_timeout)
            http_probe_response = {
                'timestamp': str(datetime.now()),
                'return_code': http_probe.status_code,
                'response_time_sec': http_probe.elapsed.total_seconds(),
                'page_content': http_probe.text
            }
        except requests.exceptions.Timeout:
            http_probe_response = {
                'timestamp': str(datetime.now()),
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


class CreateProbes:
    """
    This class is used to build Monitor Objects. When adding new Appl Protocols
    another entry should be added to this class. Since the absence of a protocol
    implementation is an unrecoverable error a NotImplementedError is raised.
    """

    def get_probe(self, hostname: str, probe_details: dict,
                  probe_proto: str) -> Probe:

        if probe_proto == 'HTTP':
            return HTTPProbe(hostname, probe_details)
        else:
            raise NotImplementedError
