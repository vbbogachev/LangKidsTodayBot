from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# === НАСТРОЙКИ (ЗАМЕНИ НА СВОИ ДАННЫЕ) ===
TOKEN = "1234567890:AAFfghijkllmnopqrstuvwxyz1234567890A"  # ← ТОКЕН ОТ @BotFather
ADMIN_CHAT_ID = 123456789  # ← ТВОЙ ID (от @userinfobot)
CHANNEL_ID = "@YourChannelName"  # ← ЮЗЕРНЕЙМ ТВОЕГО КАНАЛА

# === КОМАНДА /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 Наши программы", callback_data="programs")],
        [InlineKeyboardButton("🎯 Записаться на пробное занятие", callback_data="trial")],
        [InlineKeyboardButton("❓ Ответы на вопросы", callback_data="faq")],
        [InlineKeyboardButton("⭐ Отзывы родителей", callback_data="reviews")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет! 👋\n\n"
        "Я — бот *Детской школы иностранных языков*.\n\n"
        "Мы помогаем детям от 4 до 14 лет легко и с удовольствием выучить:\n"
        "🇬🇧 Английский  🇩🇪 Немецкий  🇫🇷 Французский\n\n"
        "Хочешь, чтобы твой ребёнок говорил на языке как носитель?\n"
        "Начни с *бесплатного пробного занятия*!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# === ОБРАБОТКА КНОПОК ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "programs":
        await query.edit_message_text(
            "📖 *Наши программы:*\n\n"
            "🔹 *Английский для малышей (4–6 лет)* — игры, песни, сказки\n"
            "🔹 *Английский для школьников (7–14 лет)* — разговор, грамматика, подготовка к экзаменам\n"
            "🔹 *Немецкий и французский* — с 8 лет\n\n"
            "✅ Мини-группы (до 6 детей)\n"
            "✅ Опытные преподаватели\n"
            "✅ Уроки онлайн и в мини-группах",
            parse_mode="Markdown"
        )

    elif query.data == "trial":
        await query.edit_message_text(
            "🎉 Отлично! Давайте запишем вашего ребёнка на *бесплатное пробное занятие*.\n\n"
            "Пожалуйста, пришлите:\n"
            "1. Имя ребёнка\n"
            "2. Возраст\n"
            "3. Язык (английский, немецкий, французский)\n"
            "4. Ваш телефон\n\n"
            "Пример:\n"
            "Маша, 6 лет, английский, +79991234567"
        )
        context.user_data['awaiting_application'] = True

    elif query.data == "faq":
        await query.edit_message_text(
            "❓ *Частые вопросы:*\n\n"
            "🔹 *Сколько длится занятие?*\n"
            "— 45 минут (малыши), 60 минут (школьники)\n\n"
            "🔹 *Сколько стоит обучение?*\n"
            "— От 1200 руб/мес в группе, от 2500 руб/занятие индивидуально\n\n"
            "🔹 *Есть ли пробное занятие?*\n"
            "— Да, бесплатно!\n\n"
            "🔹 *Где проходят занятия?*\n"
            "— Онлайн и в мини-группах в центре города."
        )

    elif query.data == "reviews":
        await query.edit_message_text(
            "⭐ *Отзывы родителей:*\n\n"
            "«Дочка ходит с удовольствием, уже говорит простые фразы!» — Анна, мама 5-летней Леры\n\n"
            "«Преподаватель — волшебник! Ребёнок сам просит идти на урок.» — Дмитрий\n\n"
            "📸 Смотрите фото и видео с занятий в нашем канале: [Перейти в канал](https://t.me/todayschool_nsk)",
            parse_mode="Markdown"
        )

# === ОБРАБОТКА СООБЩЕНИЙ (заявки) ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_application'):
        text = update.message.text
        user = update.message.from_user

        application_text = (
            f"🆕 *НОВАЯ ЗАЯВКА НА ПРОБНОЕ ЗАНЯТИЕ*\n\n"
            f"От: {user.full_name} (@{user.username})\n"
            f"Данные родителя:\n{text}\n\n"
            f"ID пользователя: {user.id}"
        )
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=application_text,
            parse_mode="Markdown"
        )

        await update.message.reply_text(
            "✅ Спасибо! Мы получили вашу заявку.\n\n"
            "Менеджер свяжется с вами в течение 24 часов, чтобы подобрать удобное время.\n\n"
            "А пока — заходите в наш канал, где мы публикуем успехи учеников: @YourChannelName"
        )

        context.user_data['awaiting_application'] = False

# === ЗАПУСК БОТА ===
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", пообщаемся))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен и готов к работе!")
    app.run_polling()

if __name__ == "__main__":
    main()
