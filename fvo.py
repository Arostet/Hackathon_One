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
    def view_users(self):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT username, location FROM users ORDER BY location")
        rows = self.cur.fetchall()
        formatted_rows = [f"{row[0]} - {row[1]}" for row in rows]
        ret_list = '\n'.join(formatted_rows)
        return ret_list
        
    def view_all_opps(self, conn):
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT * FROM opportunities")
            rows = self.cur.fetchall()
            for row in rows:
                print(row)
            self.cur.close()

    # Function to add a new user
    def add_user(self, chat_id):
        user_info = self.user_data.get(chat_id, {})
        username = user_info.get('username', 'Unknown')
        phone_number = user_info.get('phone_number', '0000000000')
        user_type = user_info.get('role', 'unknown')  
        location = user_info.get('location', 'unknown')
        volday = user_info.get('volday', '0000-00-00')

        insert_query = 'INSERT INTO users (username, phone_number, user_type, location, volday) VALUES (%s, %s, %s, %s, %s)'
        data_to_insert = (username, phone_number, user_type, location, volday)
        self.cur.execute(insert_query, data_to_insert)
        self.conn.commit()

    def add_opportunity(self, chat_id):
        opportunity_info = self.user_data.get(chat_id, {})
        title = opportunity_info.get('title', 'No Title')
        description = opportunity_info.get('description', 'No Description')
        location = opportunity_info.get('location', 'Unknown Location')
        oppday = opportunity_info.get('oppday', '0000-00-00')

        insert_query = 'INSERT INTO opportunities (title, description, location, oppday) VALUES (%s, %s, %s, %s)'
        data_to_insert = (title, description, location, oppday)
        self.cur.execute(insert_query, data_to_insert)
        self.conn.commit()

    def list_opportunities(self):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT DISTINCT location FROM opportunities ORDER BY location")
        rows = self.cur.fetchall()
        locations = [row[0] for row in rows]  
        ret_list = '\n'.join(locations)
        return ret_list
    
    def list_opps(self, chat_id):
        user_info = self.user_data.get(chat_id, {})
        self.cur = self.conn.cursor()
        volday = user_info.get('volday', '0000-00-00')
        self.cur.execute(f"SELECT title, description, location FROM opportunities WHERE oppday = '{volday}' ORDER BY location;")
        rows = self.cur.fetchall()
        opps = [row[0] for row in rows]
        ret_list = '\n'.join(opps)
        return ret_list
    

    def close_c_c(self):
        self.cur.close()
        self.conn.close()


trial = Farm()
