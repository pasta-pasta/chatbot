import logging
import sys
from logging.handlers import RotatingFileHandler



# Стартовый блок
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.responses import Response

import bot

#создаем апу, логгер и класс бота

app = FastAPI()

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                    filename="collector.error",  # Optionally, specify a file to write logs to
                    )
logger = logging.getLogger(__name__)

bot = bot.bot("YOUR_vk_TOKEN_HERE"
)

async def handle(data):
    print("Data received in handle!")
    await bot.listener.handle_update(data)


# Создаем обработчик логов
handler = RotatingFileHandler('boticon.error', maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

#Инициализация бота, любые нужные действия
@app.on_event("startup")
async def on_startup():
    await bot.init()

@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

#Смерть бота, вызывается при выключении и рестарте, сохраняет данные
@app.on_event("shutdown")
async def on_shutdown():
    bot.shutdown()

# Запросы на корневой адрес (GET, OPTIONS)
@app.get("/bot")
async def get_request():
    return "Alive!"


# Запросы на корневой адрес (POST). Вызывает обратку
@app.post("/bot")
async def post_request(request: Request):
    data = await request.json()
    try:
        await handle(data)
    except Exception as e:
        print(f"Exception! {e}")
        try:
            if data['type'] == 'confirmation':
                return Response(content="14faaa59", media_type="text/plain") #В content надо впихнуть confirmation code от группы, к которой подключаете бота.
        except:
            return Response(content="ok", media_type="text/plain")
    return Response(content="ok", media_type="text/plain")

