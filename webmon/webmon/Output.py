from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers="kafkawebmonitor-aivenhomework.aivencloud.com:13980",
    security_protocol="SSL",
    ssl_cafile="../certificates/ca.pem",
    ssl_certfile="../certificates/service.cert",
    ssl_keyfile="../certificates/service.key",
)

for i in range(1, 4):

    message = "Message Number {}".format(i)
    producer.send(
        "http_monitor", message.encode("utf-8")
    )

producer.flush()
