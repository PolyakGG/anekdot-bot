import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import asyncio

# -----------------------------
# Прямо в коде прописываем токен и ID канала
# -----------------------------
TOKEN = "MTA4ODcyODA3OTMzNTE3NDE4NQ.GlINrB.JmjyI6zil2sQeeMSR8ILeSB5qJWb6Z_n0tW9DY"          # пример: "MTAx…"
CHANNEL_ID = 1277321618313445517        # ID канала как число

# -----------------------------
# Настройка intents
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True

# Инициализация обычного бота
bot = commands.Bot(command_prefix='!', intents=intents)

# URL страницы с анекдотами
URL = "https://www.anekdot.ru/random/anekdot/"

# -----------------------------
# Событие при подключении
# -----------------------------
@bot.event
async def on_ready():
    print(f'{bot.user} подключился к Discord!')
    send_anekdots.start()  # Запуск периодической задачи

# -----------------------------
# Функция для получения анекдотов
# -----------------------------
def fetch_anekdots():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    jokes = []
    for topicbox in soup.find_all("div", class_="topicbox"):
        text_div = topicbox.find("div", class_="text")
        if text_div:
            joke_text = text_div.get_text(strip=True)
            jokes.append(joke_text)
    return jokes

# -----------------------------
# Периодическая задача: каждые 8 часов отправка анекдотов по одному каждые 5 минут
# -----------------------------
@tasks.loop(hours=1)
async def send_anekdots():
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print("❌ Канал не найден! Проверь CHANNEL_ID.")
        return

    jokes = fetch_anekdots()
    for joke in jokes:
        try:
            await channel.send(joke)
            await asyncio.sleep(300)  # 5 минут = 300 секунд
        except Exception as e:
            print(f"Ошибка при отправке: {e}")
            await asyncio.sleep(5)

# -----------------------------
# Запуск бота
# -----------------------------
bot.run(TOKEN)
