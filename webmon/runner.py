from webmon import Config
from webmon import Probe
import threading
import time


def probe_thread(probe_obj: Probe.Probe):
    """
    This routine runs th

    :param probe_obj:
    :return:
    """
    probe_conf = probe_obj.get_monitor_details()
    sleep_freq = probe_conf['FREQUENCY']

    while True:
        probe_out = probe_obj.basic_probe()
        print("Probing {}".format(probe_obj.get_hostname()))

        if isinstance(probe_obj, Probe.HTTPProbe) and \
                len(probe_conf['REGEX_MON']) > 0:
            for regex in probe_conf['REGEX_MON']:
                print(probe_obj.regex_probe(probe_out['page_content'], regex))
        time.sleep(int(sleep_freq))


def main():
    main_config = Config.UserConfig()
    probe_creator = Probe.CreateProbes()

    for host in main_config.list_hosts():
        probe_detail = main_config.get_mon_details(host)

        probe_obj = probe_creator.get_probe(
            host, probe_detail, probe_detail['PROTO']
        )

        threads = threading.Thread(
            target=probe_thread,
            args=[probe_obj])
        threads.start()


if __name__ == '__main__':
    main()
