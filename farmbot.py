import os
import telebot
from dotenv import load_dotenv
from fvo import Farm

load_dotenv()

class FarmBot:
    def __init__(self):
        self.bot_token = os.environ.get('BOT_TOKEN')
        self.bot = telebot.TeleBot(self.bot_token)
        self.user_data = {}
        self.farm = Farm(user_data=self.user_data)
        self.setup_handlers()

    def setup_handlers(self):
        self.bot.message_handler(commands=['start', 'hello'])(self.send_welcome)
        self.bot.message_handler(func=lambda message: message.content_type == 'text' and message.text.lower() == 'volunteer')(self.ask_volunteer)
        self.bot.message_handler(func=lambda message: self.user_data.get(message.chat.id, {}).get('next_step') == 'ask_city')(self.handle_city_response)
        self.bot.message_handler(func=lambda message: message.content_type == 'text' and message.text.lower() == 'farm')(self.ask_farm)
        self.bot.message_handler(func=lambda message: self.user_data.get(message.chat.id, {}).get('next_step') == 'ask_title')(self.handle_title_input)
        self.bot.message_handler(func=lambda message: self.user_data.get(message.chat.id, {}).get('next_step') == 'ask_description')(self.handle_description_input)
        self.bot.message_handler(func=lambda message: self.user_data.get(message.chat.id, {}).get('next_step') == 'ask_location')(self.handle_location_input)
        self.bot.message_handler(func=lambda message: self.user_data.get(message.chat.id, {}).get('next_step') == 'ask_username')(self.handle_username_input)
        self.bot.message_handler(func=lambda message: self.user_data.get(message.chat.id, {}).get('next_step') == 'ask_phone')(self.handle_phone_input)
        self.bot.message_handler(func=lambda message: self.user_data.get(message.chat.id, {}).get('next_step') == 'show_volunteers')(self.handle_volunteer_display)
        self.bot.message_handler(func=lambda message: True)(self.default_message)


    def send_welcome(self, message):
        self.bot.reply_to(message, "Welcome to the Farm Volunteer bot! Are you a 'farm' looking for volunteers or a 'volunteer' looking for farms? Please type your answer.")

    def ask_volunteer(self, message):
        chat_id = message.chat.id
        self.bot.reply_to(message, "Awesome! You're a volunteer looking for farms. What city are you interested in volunteering in?")
        self.update_user_data(chat_id, 'role', 'volunteer')
        self.update_user_data(chat_id, 'next_step', 'ask_city')

    def handle_city_response(self, message):
        chat_id = message.chat.id
        city = message.text.strip()
        self.update_user_data(chat_id, 'location', city)
        

        # Call list_opportunities from the Farm instance
        opportunities = self.farm.list_opportunities()
    
        # Ensure that opportunities is a string
        opportunities_message = f"Here is a list of locations that we have volunteer opportunities for you: \n \n{str(opportunities)} \n \nIf that works for you, what would you like your username to be?"
        
        self.bot.reply_to(message, opportunities_message)
        self.update_user_data(chat_id, 'next_step', 'ask_username')

    def handle_username_input(self, message):
        chat_id = message.chat.id
        username = message.text.strip()
        self.update_user_data(chat_id, 'username', username)
        self.bot.reply_to(message, "What's your phone number:")
        self.update_user_data(chat_id, 'next_step', 'ask_phone')

    def handle_phone_input(self, message):
        chat_id = message.chat.id
        phone_number = message.text.strip()
        self.update_user_data(chat_id, 'phone_number', phone_number)

        try:
            self.farm.add_user(chat_id)  
            self.bot.reply_to(message, "Thank you! We have recorded your details.")
        except Exception as e:
            self.bot.reply_to(message, "Sorry, there was an error saving your details.")
            print(f"Database error: {e}")
        
        self.update_user_data(chat_id, 'next_step', None)


    def ask_farm(self, message):
        chat_id = message.chat.id
        self.bot.reply_to(message, "Great! You're a farm looking for volunteers. What would you title this volunteer opportunity? ")
        self.update_user_data(chat_id, 'role', 'farm')
        self.update_user_data(chat_id, 'next_step', 'ask_title')

    def handle_title_input(self, message):
        chat_id = message.chat.id
        title = message.text.strip()
        self.update_user_data(chat_id, 'title', title)
        self.bot.reply_to(message, "Please enter a description for the opportunity.")
        self.update_user_data(chat_id, 'next_step', 'ask_description')

    def handle_description_input(self, message):
        chat_id = message.chat.id
        description = message.text.strip()
        self.update_user_data(chat_id, 'description', description)
        self.bot.reply_to(message, "Please enter the location for the volunteering.")
        self.update_user_data(chat_id, 'next_step', 'ask_location')

    def handle_location_input(self, message):
        chat_id = message.chat.id
        location = message.text.strip()
        self.update_user_data(chat_id, 'location', location)
        try:
            # Here you call add_user with only chat_id as it retrieves other data from user_data internally
            self.farm.add_opportunity(chat_id)  
            self.bot.reply_to(message, "Thank you! We have recorded your details. Type in 'show' if you want to see a list of volunteers that you can contact today!")
        except Exception as e:
            self.bot.reply_to(message, "Sorry, there was an error saving your details.")
            print(f"Database error: {e}")

        self.update_user_data(chat_id, 'next_step', 'show_volunteers')

    def handle_volunteer_display(self, message):
        chat_id = message.chat.id
        print("handling voll")

        try:
                volunteer_info = self.farm.view_users()  
                self.bot.reply_to(message, f"Here are some volunteers. If they are close enough to you, Enter their username to get their phone number: \n{volunteer_info} ")
        except Exception as e:
                self.bot.reply_to(message, "Sorry, there was an error saving your details.")
                print(f"Database error: {e}")

        self.update_user_data(chat_id, 'next_step', None)

    def default_message(self, message):
        self.bot.reply_to(message, "You're on your way to goodness! Please type 'farm' or 'volunteer' to proceed.")

    def update_user_data(self, chat_id, key, value):
        if chat_id not in self.user_data:
            self.user_data[chat_id] = {}
        self.user_data[chat_id][key] = value

    def start_polling(self):
        try:
            self.bot.polling()
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    farm_bot = FarmBot()
    farm_bot.start_polling()
