import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ====== KONFIGURASI ======
BOT_TOKEN = "8953132207:AAE4iCqGj9weJ80VXJWjb4WLaSEzb2aNI78"
DASHBOARD_URL = "http://localhost:8501/"

# Status perangkat (sementara disimpan di memori)
status = {"power": False}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def menu_keyboard():
    state = "🟢 ON" if status["power"] else "🔴 OFF"
    keyboard = [
        [
            InlineKeyboardButton("✅ ON", callback_data="on"),
            InlineKeyboardButton("⛔ OFF", callback_data="off"),
        ],
        [InlineKeyboardButton("📊 Dashboard", url=DASHBOARD_URL)],
    ]
    return state, InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state, markup = menu_keyboard()
    await update.message.reply_text(
        f"*Menu Kontrol*\nStatus saat ini: {state}",
        reply_markup=markup,
        parse_mode="Markdown",
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "on":
        status["power"] = True
        # TODO: kirim perintah ON ke perangkat (MQTT/HTTP/dll)
    elif query.data == "off":
        status["power"] = False
        # TODO: kirim perintah OFF ke perangkat (MQTT/HTTP/dll)

    state, markup = menu_keyboard()
    await query.edit_message_text(
        f"*Menu Kontrol*\nStatus saat ini: {state}",
        reply_markup=markup,
        parse_mode="Markdown",
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()