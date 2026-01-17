import telebot
import time
import threading
import os

# Твои данные
BOT_TOKEN = "8365918250:AAF4uKzE_T6886xS_A8YrqXtA9S6UEigvw4"
ADMIN_ID = 7469181511

bot = telebot.TeleBot(BOT_TOKEN)

def create_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    games = ["CS2", "Valorant", "Fortnite", "Apex Legends", "Roblox", "Minecraft", "GTA V", "Rust", "Другая"]
    for i in range(0, len(games), 2):
        if i+1 < len(games):
            markup.add(games[i], games[i+1])
        else:
            markup.add(games[i])
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Выбери игру для скрипта:", reply_markup=create_keyboard())

@bot.message_handler(func=lambda m: True)
def handle(message):
    game = message.text.strip()
    report = f"НОВАЯ ЗАЯВКА!\nОт: {message.from_user.first_name} (@{message.from_user.username or 'нет'})\nID: {message.from_user.id}\nИгра: {game}\nВремя: {time.strftime('%Y-%m-%d %H:%M')}"
    try:
        bot.send_message(ADMIN_ID, report)
        bot.reply_to(message, "Заявка отправлена! Скоро ответим.")
    except Exception as e:
        bot.reply_to(message, "Ошибка отправки... Попробуй позже.")

def keep_alive():
    while True:
        print("Bot alive check...")
        time.sleep(300)  # каждые 5 мин лог, помогает против некоторых таймаутов

if __name__ == "__main__":
    print("Starting Telegram Bot on Pella...")
    threading.Thread(target=keep_alive, daemon=True).start()
    
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(10)
