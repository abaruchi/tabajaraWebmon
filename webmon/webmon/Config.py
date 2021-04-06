import json
from os import getcwd
from pathlib import Path


class UserConfig(object):

    def __init__(self, config_path: str = None):

        try:
            if config_path is None:
                self.config_path = Path(getcwd()) / 'webmon/config.json'
            else:
                self.config_path = Path(config_path)

        except FileNotFoundError as e:
            print("Missing configuration file {}".format(getcwd() +
                                                         self.config_path))
            print("Error: {}".format(e))

        with self.config_path.open(mode='r') as read_file:
            config_json = json.load(read_file)
        self.config_json = config_json

    def list_hosts(self) -> list:
        """
        This method lists all hosts in config file that should be monitored.

        :return: list with hosts
        """

        return [host for host in self.config_json['HOSTS'].keys()]

    def get_mon_details(self, host: str) -> dict:
        """
        This method get monitoring details from a given host.

        :param host: the hostname to get details
        :return: dictionary with monitoring details
        """

        return self.config_json['HOSTS'].get(host, {})

    def get_aiven_conn_info(self) -> dict:
        """
        This method just returns the connection information to AIVEN
        Infrastructure.

        :return: dictionary with Aiven connection data
        """

        return self.config_json["AIVEN"]
