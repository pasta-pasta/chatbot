import logging
import sys
from logging.handlers import RotatingFileHandler



# Стартовый блок
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.responses import Response

import bot

app = FastAPI()

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                    filename="collector.error",  # Optionally, specify a file to write logs to
                    )
logger = logging.getLogger(__name__)

bot = bot.bot("vk1.a.VA2ngPKXS_oMPLbOgy0HeQmspb5XLP7XNdKkXZ1HVEvg4uJIGjC_dHgY443c__IhL0ad2RmqEgUa77lI7Gk8MZqsjUUjqdbyiTo0Fq88kLsfRw-jOpyuPuhM3uL3EGA5AM7tlMbOpqGnb41RmDqjdIGD1ouaj-gJnxbsqyV_Fhv46h-gaRoDdd8fKNT3ri7Yhs7AT5BdtiguS07uzEonZA"
)

async def handle(data):
    print("Data received in handle!")
    await bot.listener.handle_update(data)


# Create a rotating file handler that logs error messages and rotates at 5MB
handler = RotatingFileHandler('boticon.error', maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
@app.on_event("startup")
async def on_startup():
    # your initialization logic here
    await bot.init()

@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

@app.on_event("shutdown")
async def on_shutdown():
    # your initialization logic here
    bot.shutdown()

# Запросы на корневой адрес (GET, OPTIONS)
@app.get("/bot")
async def get_request():
    return "Alive!"


# Запросы на корневой адрес (POST)
@app.post("/bot")
async def post_request(request: Request):
    data = await request.json()
    try:
        await handle(data)
    except Exception as e:
        print(f"Exception! {e}")
        try:
            if data['type'] == 'confirmation':
                return Response(content="14faaa59", media_type="text/plain")
        except:
            return Response(content="ok", media_type="text/plain")
    return Response(content="ok", media_type="text/plain")

