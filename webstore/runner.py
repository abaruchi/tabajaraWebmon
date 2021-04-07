from webstore import Config, Consumer


config = Config.UserConfig()

Consumer.from_kafka(config)
