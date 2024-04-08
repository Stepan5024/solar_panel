# Используйте официальный образ Python как основу
FROM python:3.9

# Установите рабочую директорию внутри контейнера
WORKDIR /app

# Установите необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Копируйте файлы из вашей локальной машины в файловую систему контейнера
COPY . /app

# Установите необходимые зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Запустите ваш скрипт при запуске контейнера
CMD ["python", "./main_py_gui.py"]
