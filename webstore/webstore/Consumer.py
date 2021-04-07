from kafka import KafkaConsumer

from webstore import Config


# Todo: Handle different topics for different protocols
def from_kafka(config: Config.UserConfig):
    """

    :param config:
    :return:
    """
    kafka_config = config.get_service_details("KAFKA")

    consumer = KafkaConsumer(
        kafka_config["topics"][0],
        auto_offset_reset="earliest",
        bootstrap_servers=kafka_config["host"] + ":" + kafka_config["port"],
        group_id="consumer-group",
        enable_auto_commit=True,
        security_protocol="SSL",
        ssl_cafile=kafka_config["AUTH"]["ssl_cafile"],
        ssl_certfile=kafka_config["AUTH"]["ssl_certfile"],
        ssl_keyfile=kafka_config["AUTH"]["ssl_keyfile"])

    for message in consumer:
        message = message.value
        print(message.decode('utf-8'))
