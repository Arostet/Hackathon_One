import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class Purple():
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
)
        self.cur = self.conn.cursor()
    def list_opportunities(self):
        while True:
            self.cur = self.conn.cursor()
            self.cur.execute(f"SELECT * FROM opportunities")
            rows = self.cur.fetchall()
            for row in rows:
                print(row)
            self.close_c_c()

    def close_c_c(self):
         self.cur.close()
         self.conn.close()

run_one = Purple()
run_one.list_opportunities()