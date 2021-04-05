from webmon import Config

c = Config.user_config
print(c.list_hosts())
print(c.get_mon_details('https://aiven.io/'))

print("Hi there.. Im TABAJARA WebMon")
