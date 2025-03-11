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

    stores = ["rozetka", "ctrs", "foxtrot", "moyo", "comfy"]
    results = []

    for store in stores:
        cursor.execute(f"""
            SELECT id, product_name, price, url, date 
            FROM {store} 
            WHERE product_name LIKE ? 
            ORDER BY date DESC 
            LIMIT 1
        """, (f"%{iphone_name}%",))
        data = cursor.fetchone()  # Беремо тільки один найновіший запис

        if data:
            id, product_name, price, url, date = data
            results.append((store, product_name, price, url, date))

    conn.close()

    if results:
        results.sort(key=lambda x: x[2])  # Сортуємо за ціною
        response = "Ось що я знайшов:\n\n"

        for store, product_name, price, url, date in results:
            response += (
                f"📍 Магазин: {store}\n"
                f"📱 {product_name}\n"
                f"💰 Ціна: {price} грн\n"
                f"🛒 Посилання: {url}\n\n"
            )

        best = results[0]  # Найдешевший варіант
        response += f"✅ Найдешевше в {best[0]} за {best[2]} грн!\n🛒 Посилання: {best[3]}"

    else:
        response = "❌ Вибач, але я не знайшов цей iPhone у магазинах. Спробуй ще раз!"

    bot.send_message(message.chat.id, response)


bot.polling()
