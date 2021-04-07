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
        client_id="consumer-mon-client-1",
        group_id="consumer-mon-group",
        security_protocol="SSL",
        ssl_cafile=kafka_config["AUTH"]["ssl_cafile"],
        ssl_certfile=kafka_config["AUTH"]["ssl_certfile"],
        ssl_keyfile=kafka_config["AUTH"]["ssl_keyfile"])

    for _ in range(2):
        raw_msgs = consumer.poll(timeout_ms=1000)
        for tp, messages in raw_msgs.items():
            for message in messages:
                print("Received: {}".format(message.value))

    consumer.commit()
