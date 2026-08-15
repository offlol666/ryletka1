from aiogram import Bot, Dispatcher, types
from aiohttp import web

# Инициализируем бота и диспетчер
bot = Bot(token="8939932604:AAFIcBBtLsia7D956VBYQXV1z4o7kPDDDWw")
dp = Dispatcher()

# 1. Обработчик запроса от вашего WebApp
async def create_invoice_handler(request):
    cost = int(request.rel_url.query.get('cost', 10))
    
    # Создаем инвойс на оплату Telegram Stars (валюта XTR)
    invoice_link = await bot.create_invoice_link(
        title="Прокрутка рулетки",
        description=f"Оплата за прокрутку рулетки ({cost} звезд)",
        payload=f"spin_{cost}",
        currency="XTR",
        prices=[types.LabeledPrice(label="Stars", amount=cost)]
    )
    
    return web.json_response({"invoice_link": invoice_link})

# 2. Обязательный обработчик подтверждения платежа от Telegram
@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# 3. Обработчик успешного платежа (чтобы зафиксировать оплату, если нужно)
@dp.message(F.successful_payment)
async def success_payment_handler(message: types.Message):
    await message.answer("Спасибо за оплату! Удачи в рулетке 🎲")

# 4. Настройка и запуск aiohttp сервера + поллинг бота
async def main():
    app = web.Application()
    # Регистрируем тот самый путь, который запрашивает WebApp в fetch()
    app.router.add_get('/api/create-invoice', create_invoice_handler)
    
    # Запускаем веб-сервер на порту 8080 (или другом нужном)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    print("Веб-сервер запущен на порту 8080")

    # Запускаем получение обновлений для Telegram-бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
