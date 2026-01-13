# Базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /Shop

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY main.py api/ core/ models/ schemas/ services/ front_routers/ templates/ migrations/ ./

# Открываем порт
EXPOSE 8000

# Команда запуска (для FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]