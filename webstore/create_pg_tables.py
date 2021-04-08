import psycopg2
from pathlib import Path
from webstore import Config

config = Config.UserConfig('./config.json')
db_service = config.get_service_details("POSTGRESQL")
sql_query_file = Path('./create_tables.sql')

db_conn = psycopg2.connect(db_service["uri"])
db_cursor = db_conn.cursor()

r = sql_query_file.read_text()

for sql_command in r.split(";"):
    if len(sql_command) > 0:
        print(sql_command)
        db_cursor.execute(sql_command)
        db_conn.commit()
    else:
        continue
