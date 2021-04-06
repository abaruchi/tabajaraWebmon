from webmon import Config, Probe, Output
import threading
import time


def probe_thread(probe_obj: Probe.Probe, writer: Output.Output):
    """
    This routine runs th

    :param writer:
    :param probe_obj:
    :return:
    """
    probe_conf = probe_obj.get_monitor_details()
    sleep_freq = probe_conf['FREQUENCY']

    while True:
        probe_out = probe_obj.basic_probe()
        message = "host:{},rc:{},rt:{},ct:{}".format(probe_obj.get_hostname(),
                                                     probe_out["return_code"],
                                                     probe_out["response_time_sec"],
                                                     probe_out["page_content"])
        writer.write(message, probe_conf["PROTO"])

        if isinstance(probe_obj, Probe.HTTPProbe) and \
                len(probe_conf['REGEX_MON']) > 0:
            for regex in probe_conf['REGEX_MON']:
                if probe_obj.regex_probe(probe_out['page_content'], regex):
                    message = "host:{},regex_match:{}".format(
                        probe_obj.get_hostname(), regex)
                    writer.write(message, probe_conf["PROTO"])
        time.sleep(int(sleep_freq))


def main():

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
