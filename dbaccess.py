import psycopg2
import json 
from datetime import datetime, timedelta

class databaseConn(object):

    def __init__(self):

        with open(r"chess_creds.json", "r") as credentials:
            creds = json.loads(credentials.read())

        self.db_conn = psycopg2.connect(database=creds['database'],
        user=creds['user'],
        password=creds['password'],
        host=creds['host'],
        port=creds['port'])

    def execute_select(self, select_sql):

        cur = self.db_conn.cursor()

        cur.execute(select_sql)

        select_data = cur.fetchall()

        cur.close()

        return select_data

    def execute_update(self, update_sql):

        cur = self.db_conn.cursor()

        try: 
            cur.execute(update_sql)
            self.db_conn.commit()
            cur.close()

            return True 
        except Exception as e:
            print(e)
            cur.close()
            return False

    def execute_insert(self, insert_sql, data):

        cur = self.db_conn.cursor()

        try: 
            cur.execute(insert_sql, data)
            self.db_conn.commit()
            cur.close()

            return True 
        except Exception as e:
            print(e)
            cur.close()
            return False
