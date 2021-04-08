from typing import TextIO

import psycopg2

from webstore import SQL


class SQLStorer(object):
    """
    This class implements a writer to a PostgreSQL database.
    """

    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn
        self.db_cursor = conn.cursor()
        self.SQLCommand = SQL.Command()

    def http_writer(self, table: str, message: str) -> None:
        """
        This method is the writer itself. It implements some data transformation
        to the raw message and writes to the database.

        :param table: Table to write the data consumed from Kafka
        :param message: The message itself to write to the database
        """
        values = message.split(',')
        table_data = list()

        if table == "http_basic_monitor":
            for value in values:
                value_0 = value.split('::')[0]
                value_1 = value.split('::')[1]

                if value_0 == 'host':
                    table_data.append(('host', value_1))
                elif value_0 == 'rc':
                    table_data.append(('error_code', value_1))
                elif value_0 == 'ts':
                    table_data.append(('monitor_time', value_1))
                elif value_0 == 'rt':
                    table_data.append(('response_time_sec', value_1))
                else:
                    continue

        elif table == "http_regex_monitor":
            for value in values:
                value_0 = value.split('::')[0]
                value_1 = value.split('::')[1]

                if value_0 == 'host':
                    table_data.append(('host', value_1))
                elif value_0 == 'ts':
                    table_data.append(('monitor_time', value_1))
                elif value_0 == 'regex_match':
                    table_data.append(('regex_match', value_1))
                else:
                    continue
        else:
            raise NotImplementedError

        sql_insert = self.SQLCommand.insert("public." + table, table_data)
        self.db_cursor.execute(sql_insert)
        self.conn.commit()


class FileStorer(object):
    """
    This class implements mechanisms to write data from Kafta to a file. It can
    be used to test the consumer to write in a specific file.
    """

    def __init__(self, fd: TextIO):
        self.fd = fd

    def http_writer(self, monitor_type: str, message: str):

        self.fd.write(
            "http_monitor, {}: {}\n".format(monitor_type, message)
        )
        self.fd.flush()


def CreateStorer(type: str, **kwargs):
    """
    This routine is used to create objects that handlers specificities of each
    storage type.

    :param type: Storage device type
    :param kwargs: Any args that should be passed to the class in order to
                    create the connection
    :return: An instance of the storage object handler
    """
    storer = {
        "SQL": SQLStorer,
        "File": FileStorer
    }

    return storer[type](**kwargs)
