import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiohttp import web
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def create_invoice_handler(request):
    cost = int(request.rel_url.query.get('cost', 10))
    invoice_link = await bot.create_invoice_link(
        title="Прокрутка рулетки",
        description=f"Оплата за прокрутку рулетки ({cost} звезд)",
        payload=f"spin_{cost}",
        currency="XTR",
        prices=[types.LabeledPrice(label="Stars", amount=cost)]
    )
    return web.json_response({"invoice_link": invoice_link})

@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def success_payment_handler(message: types.Message):
    await message.answer("Спасибо за оплату! Удачи в рулетке 🎲")

async def main():
    app = web.Application()
    app.router.add_get('/api/create-invoice', create_invoice_handler)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080)))
    await site.start()
    print("Веб-сервер запущен")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
