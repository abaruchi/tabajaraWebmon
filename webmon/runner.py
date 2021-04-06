from webmon import Config
from webmon import Probe

c = Config.UserConfig()
probe_creator = Probe.CreateProbe()

for host in c.list_hosts():

    print("Probe: {}".format(host))
    probe_details = c.get_mon_details(host)
    http_probe = probe_creator.get_probe(host, probe_details)
    probe_result = http_probe.basic_probe()

    if len(probe_details['REGEX_MON']) > 0:
        for regex in probe_details['REGEX_MON']:
            print(http_probe.regex_probe(probe_result['page_content'], regex))

print("Hi there.. Im TABAJARA WebMon")
