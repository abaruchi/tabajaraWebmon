import threading

import psycopg2
from kafka import KafkaConsumer

from webstore import Config, Consumer, Storer


def writer_thread(protocol: str, kafka_conn: KafkaConsumer,
                  storage_writer: Storer):
    """
    This is the thread routine that runs for each monitoring protocol.

    :param protocol: The Application protocol that is being monitored
    :param kafka_conn: A kafka connection to read messages from
    :param storage_writer: The writer object that will be used to store data
                            from kafka
    """

    for message in kafka_conn:
        raw_message = message.value
        message = raw_message.decode('utf-8')
        message_parts = message.split(',')

        if protocol == 'http':
            basic_monitor = 'http_basic_monitor'
            regex_monitor = 'http_regex_monitor'
        else:
            raise NotImplementedError

        monitoring_type = message_parts[0].split('::')

        # Basic Monitoring
        if monitoring_type[1] == 'basic':
            storage_writer.http_writer(basic_monitor, message)

        # Regex Monitoring
        if monitoring_type[1] == 'regex':
            storage_writer.http_writer(regex_monitor, message)


def main():
    """
    This routine performs the proper class instantiation and threads to produce
    data to an external system. Steps performed here are:

    1. Gather all necessary information from configuration files
    2. For each Kafka's topic (which represents a different Application
        Protocol):
        2.1 Creates a Kafka connection to the proper topic
        2.2 Creates a connection with DB and pass it to a Writer Object (that
            is responsible to write to a PostgreSQL DB or any other persistent
            storage that implements the interfaces defined)
        2.3 Creates a thread to read from the topic and writes it to specific
            places (defined when creating the

    3. For each host to monitor:
       3.1 A monitor instance is created
       3.2 A thread is created with the monitor instance and kafka writer
    """

    config = Config.UserConfig()

    kafka_service = config.get_service_details("KAFKA")
    db_service = config.get_service_details("POSTGRESQL")

    # Each topic in kafka represents a different Appl protocol
    # For each Protocol, we want different threads
    for topic in kafka_service["topics"]:
        protocol = topic.split("_")[0]

        # Creates the kafka consumer
        kafka_consumer = Consumer.kafka_consumer(config, topic)

        # Creates a Connection with DB
        # db_conn = psycopg2.connect(db_service["uri"])
        # db_storer = Storer.CreateStorer("SQL", conn=db_conn)
        #
        # threads = threading.Thread(
        #     target=writer_thread,
        #     args=[protocol, kafka_consumer, db_storer]
        # )
        # threads.start()

        # Creates a file writer - uncomment it to write it to a local file
        monitor_fd = open('./http_monitoring', 'w+')
        file_storer = Storer.CreateStorer("File", fd=monitor_fd)
        threads = threading.Thread(
            target=writer_thread,
            args=[protocol, kafka_consumer, file_storer]
        )
        threads.start()


if __name__ == '__main__':
    main()
