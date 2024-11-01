FROM python:3.11

ADD . /overjoyed
WORKDIR /overjoyed
RUN pip install -r requirements.txt

# Установка необходимых пакетов
RUN apt-get update \
    && apt-get install -y \
        espeak \
        vorbis-tools \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python", "-m", "overjoyed"]  # Запускаем вашего бота
