import json
from os import getcwd
from pathlib import Path


class UserConfig(object):

    def __init__(self, config_path: str = None):

        try:
            if config_path is None:
                self.config_path = Path(getcwd()) / 'webstore/config.json'
            else:
                self.config_path = Path(config_path)

        except FileNotFoundError as e:
            print("Missing configuration file {}".format(getcwd() +
                                                         self.config_path))
            print("Error: {}".format(e))

        with self.config_path.open(mode='r') as read_file:
            config_json = json.load(read_file)
        self.config_json = config_json

    def list_services(self) -> list:
        """
        This method lists all services in config file.

        :return: list with services
        """

        return [service for service in self.config_json['SERVICES'].keys()]

    def get_service_details(self, service: str) -> dict:
        """
        This method get service details.

        :param service: the service to gather details
        :return: dictionary with service details
        """

        return self.config_json['SERVICES'].get(service, {})
