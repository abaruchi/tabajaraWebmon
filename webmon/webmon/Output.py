from kafka import KafkaProducer
from kafka.errors import KafkaError


class Output(object):
    """
    This abstract class must be used to implement mechanisms to Output the
    probed data to any given system (i.e. kafka, Database, Object Storage, etc)
    """

    def write(self, message: str, protocol_monitor: str = '') -> None:
        """
        This method is used to write a message to the system.

        :param message: Message to write to the system
        :param protocol_monitor: The protocol used to probe the monitored host.
        """
        pass

    def __connection_validation(self) -> bool:
        """
        This method is used to validate the connection data to a system. Since
        each system has different methods to connect, it should be implemented
        properly

        :return: True when the connection is fine, False otherwise
        """
        pass


class ToKafka(Output):

    def __init__(self, connection: dict):
        self.connection_data = connection

        if not self.__connection_validation():
            raise ConnectionAbortedError

        self.connection = self.__connect()

    def __connection_validation(self) -> bool:
        auth_fields = ["ssl_cafile", "ssl_certfile", "ssl_keyfile"]
        conn_fields = ["host", "port"]

        for auth_field in auth_fields:
            if auth_field not in self.connection_data["AUTH"]:
                return False

        for conn_field in conn_fields:
            if conn_field not in self.connection_data["CONNECTION"]:
                return False
        return True

    def __connect(self):
        """
        This method connects to a kafka instance and return the connection
        to be used
        :return:
        """
        connection_info = self.connection_data["CONNECTION"]
        auth_info = self.connection_data["AUTH"]

        producer = KafkaProducer(
            bootstrap_servers=connection_info["host"] + connection_info["port"],
            security_protocol="SSL",
            ssl_cafile=auth_info["ssl_cafile"],
            ssl_certfile=auth_info["ssl_certfile"],
            ssl_keyfile=auth_info["ssl_keyfile"])
        return producer

    def write(self, message: str, protocol_monitor: str = '') -> None:

        if len(protocol_monitor) == 0:
            raise ValueError

        kafka_topic = protocol_monitor.lower() + "_monitor"
        try:
            self.connection.send(
                kafka_topic, message.encode("utf-8")
            )
            self.connection.flush()
        except KafkaError as e:
            print("Error to Write to Topic {}.".format(kafka_topic))
            print("Error: {}".format(e))
