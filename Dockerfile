# Используем официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Открываем порт, на котором будет работать приложение
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]

