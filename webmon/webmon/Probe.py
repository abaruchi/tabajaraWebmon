

class Probe(object):

    def __init__(self, host: str, monitor_conf: dict):

        self.host = host
        self.monitor_conf = monitor_conf

    def basic_probe(self):
        pass


class HTTPProbe(Probe):

    def basic_probe(self):
        print("Basic Probe - ")

    def regex_probe(self):
        pass


def create_monitor(app_protocol: str = 'HTTP', **kwargs):
    """

    """

    probe = {
        'HTTP': HTTPProbe
    }

    try:
        probe_obj = probe[app_protocol](**kwargs)
        return probe_obj
    except KeyError as e:
        print("Protocol {} Probe not Implemented".format(app_protocol))
        print("Error: {}".format(e))
