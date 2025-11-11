#!/usr/bin/env python3
"""
TimeKeeper Telegram Backup Bot
Простий бот для авторизації та зберігання бекапів
"""

import os
import logging
import random
import json
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = "8491626430:AAFcomI07hJc-sEWKPMgc9G2qf38ZurV73E"

# Файл для зберігання кодів
CODES_FILE = "auth_codes.json"

# Словник для зберігання кодів авторизації
auth_codes = {}

def load_codes():
    """Завантажує коди з файлу"""
    global auth_codes
    try:
        if os.path.exists(CODES_FILE):
            with open(CODES_FILE, 'r') as f:
                auth_codes = json.load(f)
                # Видаляємо старі коди (старше 5 хвилин)
                current_time = time.time()
                auth_codes = {k: v for k, v in auth_codes.items() 
                             if current_time - v.get('timestamp', 0) < 300}
    except Exception as e:
        logger.error(f"Error loading codes: {e}")
        auth_codes = {}

def save_codes():
    """Зберігає коди в файл"""
    try:
        with open(CODES_FILE, 'w') as f:
            json.dump(auth_codes, f)
    except Exception as e:
        logger.error(f"Error saving codes: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /start - генерує код авторизації"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Завантажуємо існуючі коди
    load_codes()
    
    # Генеруємо 6-значний код
    code = str(random.randint(100000, 999999))
    
    # Зберігаємо код з інформацією про користувача
    auth_codes[code] = {
        'chat_id': chat_id,
        'user_name': f"{user.first_name} {user.last_name or ''}".strip(),
        'username': user.username,
        'timestamp': time.time()
    }
    
    # Зберігаємо в файл
    save_codes()
    
    welcome_message = f"""
🔐 <b>Код авторизації TimeKeeper</b>

Ваш код: <code>{code}</code>

📱 <b>Що робити далі:</b>
1. Відкрийте додаток TimeKeeper
2. Налаштування → Дані → Telegram Backup
3. Введіть цей код
4. Натисніть "Підключити"

⏱ Код дійсний 5 хвилин

✅ Після підключення всі бекапи будуть автоматично зберігатись тут!
"""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='HTML'
    )
    
    logger.info(f"Generated code {code} for user {user.first_name} (chat_id: {chat_id})")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник текстових повідомлень"""
    text = update.message.text.strip()
    
    help_message = """
ℹ️ <b>Як підключитись:</b>

1. Натисніть /start щоб отримати код
2. Введіть код в додатку TimeKeeper
3. Готово!

📦 Всі ваші бекапи будуть зберігатись в цьому чаті.
"""
    
    await update.message.reply_text(help_message, parse_mode='HTML')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /help"""
    help_text = """
📖 <b>Довідка TimeKeeper Backup Bot</b>

<b>Команди:</b>
/start - Почати роботу з ботом
/help - Показати цю довідку
/status - Перевірити статус підключення

<b>Як користуватись:</b>
1. Підключіть бота в додатку TimeKeeper
2. Бот автоматично зберігатиме ваші бекапи
3. Всі файли будуть у цьому чаті
4. Ви зможете завантажити їх в будь-який момент

<b>Безпека:</b>
• Дані зберігаються тільки у вашому чаті
• Ніхто інший не має доступу
• Файли зашифровані Telegram

Якщо у вас виникли питання, зверніться до розробника: @deonisiyon
"""
    
    await update.message.reply_text(
        help_text,
        parse_mode='HTML'
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /status"""
    chat_id = update.effective_chat.id
    
    # Тут можна додати перевірку чи користувач авторизований
    # Поки що просто показуємо базову інформацію
    
    status_text = f"""
📊 <b>Статус підключення</b>

Chat ID: <code>{chat_id}</code>

Якщо ви підключили бота в додатку, всі бекапи будуть автоматично надсилатись в цей чат.

Для повторного підключення використайте команду /start
"""
    
    await update.message.reply_text(
        status_text,
        parse_mode='HTML'
    )


def main() -> None:
    """Запуск бота"""
    # Створюємо додаток
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Додаємо обробники
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаємо бота
    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
