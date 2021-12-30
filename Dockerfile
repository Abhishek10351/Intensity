FROM python:3
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . My_bot/
WORKDIR /My_bot
CMD python3 bot.py