from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

# Укажите токен вашего бота и ID админа
BOT_TOKEN = "7642920430:AAFw9JigCoxk2OhdwJo04U_7aJLae8-gtBE"
ADMIN_ID = 702925787

# Приветственное сообщение
WELCOME_MESSAGE_RU = (
    "👋 Привет! Вы можете поделиться своими мыслями, проблемами или предложениями по поводу нашего вуза, студентов или преподавателей.\n\n"
    "📝 Напишите всё, что считаете важным. Ваш текст останется **анонимным**, его прочитает только директор или его заместитель.\n\n"
    "Когда закончите, нажмите кнопку «📨 Завершить и отправить»."
)

WELCOME_MESSAGE_UZ = (
    "👋 Salom! Universitetimiz, talabalar yoki o'qituvchilar haqidagi fikrlaringiz, muammolaringiz yoki takliflaringizni biz bilan baham ko'rishingiz mumkin.\n\n"
    "📝 O'zingiz muhim deb hisoblagan hamma narsani yozing. Sizning matningiz **maxfiy** qoladi, uni faqat direktor yoki uning o'rinbosari o'qiydi.\n\n"
    "Yakunlash uchun «📨 Yakunlash va jo'natish» tugmasini bosing."
)

# Ответ на /start
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [["📨 Завершить и отправить"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(WELCOME_MESSAGE_RU, reply_markup=reply_markup)
    await update.message.reply_text(WELCOME_MESSAGE_UZ)

# Сбор сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    if user_message == "📨 Завершить и отправить":
        collected_text = context.user_data.get("messages", [])
        if collected_text:
            # Отправляем админу собранные сообщения
            full_message = "\n\n".join(collected_text)
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"📩 Новое анонимное сообщение:\n\n{full_message}"
            )
            await update.message.reply_text("✅ Ваши мысли успешно отправлены. Спасибо!")
            context.user_data.clear()  # Очищаем данные пользователя
        else:
            await update.message.reply_text("❌ Вы ещё ничего не написали.")
    else:
        # Сохраняем сообщение пользователя
        if "messages" not in context.user_data:
            context.user_data["messages"] = []
        context.user_data["messages"].append(user_message)
        await update.message.reply_text("✍️ Ваше сообщение записано. Продолжайте или нажмите «📨 Завершить и отправить».")

# Основная функция запуска бота
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()

