from kafka import KafkaConsumer

from webstore import Config


def kafka_consumer(config: Config.UserConfig, topic: str) -> KafkaConsumer:
    """
    This function connects to the Kafka cluster and gather messages for
    a specific topic. This routine can be called for different topics (each
    topic can be a different protocol, for example).

    :param topic: The kafka topic to gather message
    :param config: A configuration instance to retrieve kafka connection info
    :return: A KafkaConsumer instance to be used by any client
    """
    kafka_config = config.get_service_details("KAFKA")

    consumer = KafkaConsumer(
        topic,
        auto_offset_reset="earliest",
        bootstrap_servers=kafka_config["host"] + ":" + kafka_config["port"],
        group_id="consumer-group",
        enable_auto_commit=True,
        security_protocol="SSL",
        ssl_cafile=kafka_config["AUTH"]["ssl_cafile"],
        ssl_certfile=kafka_config["AUTH"]["ssl_certfile"],
        ssl_keyfile=kafka_config["AUTH"]["ssl_keyfile"])

    return consumer
