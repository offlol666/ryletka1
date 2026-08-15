import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiohttp import web
from aiohttp_cors import setup as cors_setup, ResourceOptions
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def create_invoice_handler(request):
    try:
        cost = int(request.rel_url.query.get('cost', 10))
        invoice_link = await bot.create_invoice_link(
            title="Прокрутка рулетки",
            description=f"Оплата за прокрутку рулетки ({cost} звезд)",
            payload=f"spin_{cost}",
            currency="XTR",
            prices=[types.LabeledPrice(label="Stars", amount=cost)]
        )
        return web.json_response({"invoice_link": invoice_link})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def success_payment_handler(message: types.Message):
    await message.answer("Спасибо за оплату! Удачи в рулетке 🎲")

async def main():
    app = web.Application()
    
    # Настраиваем CORS, чтобы мини-приложение могло стучаться к серверу
    cors = cors_setup(app, defaults={
        "*": ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })

    # Добавляем маршрут
    resource = app.router.add_get('/api/create-invoice', create_invoice_handler)
    cors.add(resource)

    # Получаем порт от Render (по умолчанию 10000)
    port = int(os.environ.get("PORT", 10000))
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Веб-сервер запущен на порту {port}")

    # Запускаем поллинг бота
    # Удаляем вебхуки перед поллингом, чтобы избежать TelegramConflictError
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
