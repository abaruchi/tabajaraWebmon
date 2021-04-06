import threading
import time

from webmon import Config, Output, Probe


def probe_thread(probe_obj: Probe.Probe, writer: Output.Output):
    """
    This routine is the thread that performs the monitor actions, according
    to the monitor object and writes it using the writer object to the proper
    place.

    :param writer: An object that encapsulates all necessary methods to write
                    the monitor data to an external system
    :param probe_obj: An object that encapsulates all necessary methods to
                        monitor a specific host
    """
    probe_conf = probe_obj.get_monitor_details()
    sleep_freq = probe_conf['FREQUENCY']

    while True:
        probe_out = probe_obj.basic_probe()
        message = "host:{},ts:{}, rc:{},rt:{},ct:{}".format(probe_obj.get_hostname(),
                                                            probe_out["timestamp"],
                                                            probe_out["return_code"],
                                                            probe_out["response_time_sec"],
                                                            probe_out["page_content"])
        writer.write(message, probe_conf["PROTO"])

        if isinstance(probe_obj, Probe.HTTPProbe) and \
                len(probe_conf['REGEX_MON']) > 0:
            for regex in probe_conf['REGEX_MON']:
                if probe_obj.regex_probe(probe_out['page_content'], regex):
                    message = "host:{}, ts:{}, regex_match:{}".format(
                        probe_obj.get_hostname(), probe_out["timestamp"], regex)
                    writer.write(message, probe_conf["PROTO"])
        time.sleep(int(sleep_freq))


def main():
    """
    This routine performs the proper class instantiation and threads to produce
    data to an external system. Steps performed here are:

    1. Gather all necessary information from configuration files
    2. Creates an instance of a Kafka Producer (writer)
    3. For each host to monitor:
       3.1 A monitor instance is created
       3.2 A thread is created with the monitor instance and kafka writer
    """
    main_config = Config.UserConfig()
    probe_creator = Probe.CreateProbes()

    writer = Output.ToKafka(main_config.get_aiven_conn_info())

    for host in main_config.list_hosts():
        probe_detail = main_config.get_mon_details(host)

        probe_obj = probe_creator.get_probe(
            host, probe_detail, probe_detail['PROTO']
        )

        threads = threading.Thread(
            target=probe_thread,
            args=[probe_obj, writer])
        threads.start()


if __name__ == '__main__':
    main()
