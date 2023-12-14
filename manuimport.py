import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class MenuItem():
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
)
        self.cur = self.conn.cursor()
    def run_program(self):
        while True:
            self.user_input = input("What command do you want to run? --0 to exit:-) \n 1 for VALUES \n 2 for DELETE \n 3 for ADD \n 4 for UPDATE")
            if self.user_input == '0':
                print("Exiting.")
                break
            elif self.user_input == '1':
                self.cur.execute("SELECT * FROM users")
                rows = self.cur.fetchall()
                for row in rows:
                    print(row)
            elif self.user_input == '2':
                u_value = input("Which user are you looking to delete?")
                self.cur.execute(f"DELETE FROM menu_items WHERE id = {u_value}")
                self.conn.commit()
            elif self.user_input == '3':
                item_name = input("What is the item's name?")
                item_price = input("What is the item's price?")
                insert_query = 'INSERT INTO menu_items (item_name, item_price) VALUES (%s, %s)'
                data_to_insert = (item_name, item_price)
                self.cur.execute(insert_query, data_to_insert) 
                self.conn.commit()   
            elif self.user_input == '4':
                user_input_id = input("What is the id of the item you want to change?")
                new_name = input("What is the new name for this item?")
                new_price = input("What is the new price of this item?")
                self.cur.execute(f"UPDATE menu_items SET item_name = '{new_name}', item_price = {new_price} WHERE id = {user_input_id}")
        self.close_c_c()

    def close_c_c(self):
         self.cur.close()
         self.conn.close()

run_one = MenuItem()
run_one.run_program()