# AI Bot with GigaChat

Бот для Telegram с интеграцией GigaChat AI и Redis для хранения истории сообщений.

## Функциональность

- 💬 Чат с AI ассистентом на основе GigaChat
- 🧠 Сохранение контекста разговора с помощью Redis
- 🔄 Управление состояниями через FSM
- 🐳 Docker контейнеризация

## Предварительные требования

- Docker и Docker Compose
- Telegram Bot Token от [@BotFather](https://t.me/BotFather)
- Учетные данные GigaChat API

## Установка и запуск

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/bulat-nitaliev/ai-bot.git
   cd ai-bot
   ```
Настройте переменные окружения

Создайте файл .env в корневой директории:

```
BOT_TOKEN=your_telegram_bot_token_here
GIGACHAT_CREDENTIALS=your_gigachat_credentials_here
REDIS_URL=redis://redis:6379/0
```
Запустите приложение

```
docker-compose up -d
```
Проверьте логи

```
docker-compose logs -f bot
```
Структура проекта
```text
ai-bot/
│
├── main.py              # Точка входа
├── handlers.py     # Обработчики сообщений
├── state.py             # Состояния FSM
├── keyboards/
│      └── reply.py         # Клавиатуры
├── utils.py             # Утилиты
├── chat.py                  # Логика работы с GigaChat
├── config.py                # Конфигурация
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```
Команды бота
```
/start - Начать работу с ботом

"New chat" - Начать новый чат
```
Настройка Redis
Redis автоматически настраивается через Docker Compose:

Порт: 6379

Сохранение данных включено (AOF)

Данные сохраняются в volume redis_data

Мониторинг и логи
Логи приложения: docker-compose logs -f bot

Логи Redis: docker-compose logs -f redis

Данные Redis сохраняются в volume

Обновление
```
docker-compose down
docker-compose pull
docker-compose up -d
```
Переменные окружения
Переменная	Описание	Обязательная
BOT_TOKEN	Токен Telegram бота	Да
GIGACHAT_CREDENTIALS	Учетные данные GigaChat API	Да
REDIS_URL	URL для подключения к Redis	Нет (значение по умолчанию)
Разработка
Для локальной разработки:

Убедитесь, что Redis запущен:

```
docker-compose up -d redis
```
Установите зависимости:

```
pip install -r requirements.txt
```
Запустите бота:

```
python main.py
```
Troubleshooting
Бот не запускается
Проверьте правильность BOT_TOKEN

Убедитесь, что Redis запущен

Проверьте логи: docker-compose logs bot

Ошибки подключения к Redis
Убедитесь, что Redis контейнер запущен

Проверьте переменную REDIS_URL

Ошибки GigaChat API
Проверьте правильность учетных данных

Убедитесь, что API ключ активен

text

## Необходимые изменения в коде

Также вам нужно обновить `config.py` для поддержки Redis:

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")
    GIGACHAT_CREDENTIALS: str = Field(..., env="GIGACHAT_CREDENTIALS")
    REDIS_URL: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    
    class Config:
        env_file = ".env"

settings = Settings()
И обновить импорты в chat.py:

python
from langchain_community.chat_message_histories import RedisChatMessageHistory
# ... остальные импорты
from config import settings

def get_redis_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(
        session_id=session_id,
        url=settings.REDIS_URL,
        ttl=3600  # 1 час
    )

# Замените InMemoryChatMessageHistory на Redis
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_redis_history,  # Используем Redis вместо памяти
    input_messages_key="question", 
    history_messages_key="history"
)