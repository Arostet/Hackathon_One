import psycopg2
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Farm():
    def __init__(self, user_data=None) -> None:
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        self.cur = self.conn.cursor()
        self.user_data = user_data
        
        # Function to view all users
    def view_all_users(self, conn):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
        self.cur.close()

    # Function to add a new user
    def add_user(self, chat_id):
        user_info = self.user_data.get(chat_id, {})
        username = user_info.get('username', 'Unknown')
        phone_number = user_info.get('phone_number', '0000000000')
        user_type = user_info.get('role', 'unknown')  # 'farm' or 'volunteer'
        insert_query = 'INSERT INTO users (username, phone_number, user_type) VALUES (%s, %s, %s)'
        data_to_insert = (username, phone_number, user_type)
        self.cur.execute(insert_query, data_to_insert)
        self.conn.commit()

    def add_opportunity(self, chat_id):
        opportunity_info = self.user_data.get(chat_id, {})
        title = opportunity_info.get('title', 'No Title')
        description = opportunity_info.get('description', 'No Description')
        location = opportunity_info.get('location', 'Unknown Location')

        insert_query = 'INSERT INTO opportunities (title, location) VALUES (%s, %s)'
        # Assuming user_id is also stored in user_data or retrieved differently
        user_id = opportunity_info.get('user_id', 0)
        data_to_insert = (user_id, title, description, location)
        self.cur.execute(insert_query, data_to_insert)
        self.conn.commit()
    # def add_user(self):
    #     username = 
    #     phone_number = 
    #     insert_query = 'INSERT INTO menu_items (item_name, item_price) VALUES (%s, %s)'
    #     data_to_insert = (item_name, item_price)
    #     self.cur.execute(insert_query, data_to_insert) 
    #     self.conn.commit()   
    
    def list_opportunities(self, city):
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT location FROM opportunities")
        rows = self.cur.fetchall()
        for row in rows:
            return row
        

    def close_c_c(self):
        self.cur.close()
        self.conn.close()


                # item_name = 
                # item_price = 
                # insert_query = 'INSERT INTO menu_items (item_name, item_price) VALUES (%s, %s)'
                # data_to_insert = (item_name, item_price)
                # self.cur.execute(insert_query, data_to_insert) 
                # self.conn.commit()   
        
trial = Farm()
