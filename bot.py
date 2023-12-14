import os
import psycopg2
import telebot
from dotenv import load_dotenv
from tests import Purple 
load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

def update_user_data(chat_id, key, value):
    if chat_id not in user_data:
        user_data[chat_id] = {}
    user_data[chat_id][key] = value

    #check with print to see that data is storing.
    # print(f"Updated user_data for {chat_id}: {user_data[chat_id]}")  # Logging the update
# def save_farm_data(chat_id):
#     if user_data[chat_id].get('role') == 'farm':
#         farm_data = user_data[chat_id]
#         # List of attributes to save
#         attributes = ['title', 'description', 'location', 'start_date', 'duration_days']
#         for attribute in attributes:
#             # Open a file for each attribute
#             with open(f'{attribute}_data.txt', 'a') as file:
#                 if attribute in farm_data:
#                     # Write the data to the file
#                     file.write(f"Farm ID: {chat_id}, {attribute.capitalize()}: {farm_data[attribute]}\n")

# def list_opportunities(city):
#     opportunities = {
#         'New York': ['Opportunity 1', 'Opportunity 2'],
#         'Los Angeles': ['Opportunity 3', 'Opportunity 4'],
#     }
#     return "\n".join(opportunities.get(city, ["No opportunities found for this city."]))
#opening message
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Farm Volunteer bot! Are you a 'farm' looking for volunteers or a 'volunteer' looking for farms? Please type your answer.")

#if the reply is volunteer...
@bot.message_handler(func=lambda message: message.content_type == 'text' and message.text.lower() == 'volunteer')
def ask_volunteer(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Awesome! You're a volunteer looking for farms. What city are you interested in volunteering in?")
    update_user_data(chat_id, 'role', 'volunteer')
    update_user_data(chat_id, 'next_step', 'ask_city')
#if it is volunteer, next step:
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('next_step') == 'ask_city')
def handle_city_response(message):
    chat_id = message.chat.id
    city = message.text.strip() #city is what the user types // like a input()
    update_user_data(chat_id, 'city', city)
    opportunities = list_opportunities(city)
    bot.reply_to(message, opportunities)
    update_user_data(chat_id, 'next_step', None)
#if the reply is farm, add that information to dictionary here
@bot.message_handler(func=lambda message: message.content_type == 'text' and message.text.lower() == 'farm')
def ask_farm(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Great! You're a farm looking for volunteers. What would you title this volunteer opportunity? ")
    update_user_data(chat_id, 'role', 'farm')
    update_user_data(chat_id, 'next_step', 'ask_title')
#if farm, ask title
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('next_step') == 'ask_title')
def handle_title_input(message):
    chat_id = message.chat.id
    title = message.text.strip()
    update_user_data(chat_id, 'title', title)
    bot.reply_to(message, "Please enter a description for the opportunity.")
    update_user_data(chat_id, 'next_step', 'ask_description')
#step 3 for farm
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('next_step') == 'ask_description')
def handle_description_input(message):
    chat_id = message.chat.id
    description = message.text.strip()
    update_user_data(chat_id, 'description', description)
    bot.reply_to(message, "Please enter the location for the volunteering.")
    update_user_data(chat_id, 'next_step', 'ask_location')
#Step 4:
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('next_step') == 'ask_location')
def handle_location_input(message):
    chat_id = message.chat.id
    location = message.text.strip()
    update_user_data(chat_id, 'location', location)
    bot.reply_to(message, "Please enter the start date for the opportunity (YYYY-MM-DD):")
    update_user_data(chat_id, 'next_step', 'ask_start_date')
# Step 5:
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('next_step') == 'ask_start_date')
def handle_start_date_input(message):
    chat_id = message.chat.id
    start_date = message.text.strip()
    update_user_data(chat_id, 'start_date', start_date)
    bot.reply_to(message, "Please enter the duration (in days) for the opportunity.")
    update_user_data(chat_id, 'next_step', 'ask_duration_days')
#Step 6
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('next_step') == 'ask_duration_days')
def handle_duration_days_input(message):
    chat_id = message.chat.id
    duration_days = message.text.strip()
    update_user_data(chat_id, 'duration_days', duration_days)
    bot.reply_to(message, "Thank you! We have recorded the opportunity details and will try and match you with volunteers ASAP.")
    update_user_data(chat_id, 'next_step', None)  # Reset or set the next step

# Default message handler at the end
@bot.message_handler(func=lambda message: True)
def default_message(message):
    bot.reply_to(message, "Please type 'farm' or 'volunteer' to proceed.")

try:
    bot.polling()
except Exception as e:
    print("An error occurred:", e)
