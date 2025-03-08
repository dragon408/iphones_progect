import telebot
import sqlite3

bot = telebot.TeleBot('7682978624:AAGdy_BuniNZG29a_x8JiCTNeM_FLAA9qYU')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привіт! Введи назву iPhone, який тебе цікавить, і я знайду для тебе найкращу ціну!")


@bot.message_handler(content_types=['text'])
def find_iphone(message):
    iphone_name = message.text.strip()
    conn = sqlite3.connect('../settings/stores.db')
    cursor = conn.cursor()

    stores = ['comfy', 'foxtrot', 'moyo']  # Додай інші магазини, якщо треба
    results = []

    for store in stores:
        cursor.execute(f"SELECT product_name, price, url FROM {store} WHERE product_name LIKE ?", (f"%{iphone_name}%",))
        data = cursor.fetchall()
        if data:
            for row in data:
                product_name, price, url = row
                results.append((product_name, price, store, url))

    conn.close()

    if results:
        results.sort(key=lambda x: x[1])  # Сортуємо за ціною
        response = "Ось що я знайшов:\n\n"
        for product_name, price, store, url in results:
            response += (
                f"📍 Магазин: {store}\n"
                f"📱 {product_name}\n"
                f"💰 Ціна: {price} грн\n"
                f"🛒 Посилання: {url}\n\n"
            )

        best = results[0]
        response += f"✅ Найдешевше в {best[2]} за {best[1]} грн!\n🛒 Посилання: {best[3]}"

    else:
        response = "❌ Вибач, але я не знайшов цей iPhone у магазинах. Спробуй ще раз!"

    bot.send_message(message.chat.id, response)


bot.polling()
