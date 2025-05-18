# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем библиотеки Python
RUN pip install psycopg2

# Копируем ваш скрипт в контейнер
COPY analysis.py .

# Команда для запуска скрипта
CMD ["python", "analysis.py"]
