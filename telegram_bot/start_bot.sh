#!/bin/bash

# TimeKeeper Telegram Bot Starter Script

echo "🤖 Starting TimeKeeper Telegram Backup Bot..."

# Перевірка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Перевірка pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

# Встановлення залежностей
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Запуск бота
echo "✅ Starting bot..."
python3 bot.py
