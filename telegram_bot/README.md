# TimeKeeper Telegram Backup Bot

Простий Telegram бот для автоматичного збереження бекапів TimeKeeper.

## Встановлення

1. Встановіть Python 3.8 або новіше
2. Встановіть залежності:
```bash
pip install -r requirements.txt
```

## Запуск

```bash
python bot.py
```

Або зробіть файл виконуваним:
```bash
chmod +x bot.py
./bot.py
```

## Запуск у фоновому режимі

### На сервері (Linux/macOS):

```bash
nohup python bot.py > bot.log 2>&1 &
```

### Використання systemd (Linux):

Створіть файл `/etc/systemd/system/timekeeper-bot.service`:

```ini
[Unit]
Description=TimeKeeper Telegram Backup Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/telegram_bot
ExecStart=/usr/bin/python3 /path/to/telegram_bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Потім:
```bash
sudo systemctl daemon-reload
sudo systemctl enable timekeeper-bot
sudo systemctl start timekeeper-bot
```

## Як це працює

1. Користувач відкриває додаток TimeKeeper
2. В налаштуваннях вибирає "Telegram Backup"
3. Отримує 6-значний код авторизації
4. Відкриває бота в Telegram та надсилає /start
5. Надсилає код боту
6. Повертається в додаток та підтверджує авторизацію
7. Бот автоматично зберігає всі бекапи в приватному чаті

## Безпека

- Всі дані зберігаються тільки в приватних чатах користувачів
- Коди авторизації дійсні лише 5 хвилин
- Файли захищені шифруванням Telegram
- Бот не має доступу до даних інших користувачів

## Підтримка

Розробник: [@deonisiyon](https://t.me/deonisiyon)
