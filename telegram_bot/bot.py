#!/usr/bin/env python3
"""
TimeKeeper Telegram Backup Bot
Простий бот для авторизації та зберігання бекапів
"""

import os
import logging
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

# Словник для зберігання кодів авторизації
auth_codes = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /start"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    welcome_message = f"""
👋 Привіт, {user.first_name}!

Я TimeKeeper Backup Bot - ваш помічник для автоматичного збереження бекапів.

🔐 <b>Як підключитись:</b>
1. Відкрийте додаток TimeKeeper
2. Перейдіть в Налаштування → Дані → Telegram Backup
3. Натисніть "Підключити Telegram"
4. Отримайте 6-значний код
5. Надішліть мені цей код

📦 <b>Що я вмію:</b>
• Автоматично зберігати ваші бекапи
• Надсилати файли з історією робочих сесій
• Захищати ваші дані від втрати

🔒 <b>Безпека:</b>
Всі дані зберігаються тільки у вашому приватному чаті. Ніхто інший не має до них доступу.

Надішліть мені код авторизації з додатку!
"""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='HTML'
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник текстових повідомлень"""
    text = update.message.text.strip()
    chat_id = update.effective_chat.id
    user = update.effective_user
    
    # Перевіряємо чи це код авторизації (6 цифр)
    if text.isdigit() and len(text) == 6:
        # Зберігаємо код для перевірки з додатку
        auth_codes[text] = {
            'chat_id': chat_id,
            'user_name': f"{user.first_name} {user.last_name or ''}".strip(),
            'username': user.username
        }
        
        success_message = f"""
✅ <b>Код отримано!</b>

Тепер поверніться в додаток TimeKeeper та натисніть кнопку "Підтвердити авторизацію".

Ваш код: <code>{text}</code>

⏱ Код дійсний протягом 5 хвилин.
"""
        
        await update.message.reply_text(
            success_message,
            parse_mode='HTML'
        )
        
        logger.info(f"Auth code {text} received from user {user.first_name} (chat_id: {chat_id})")
    else:
        # Якщо це не код авторизації
        help_message = """
❓ Надішліть мені 6-значний код авторизації з додатку TimeKeeper.

Щоб отримати код:
1. Відкрийте TimeKeeper
2. Налаштування → Дані → Telegram Backup
3. Натисніть "Підключити Telegram"
4. Скопіюйте код та надішліть мені

Або використайте команду /start для детальної інформації.
"""
        await update.message.reply_text(help_message)


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
