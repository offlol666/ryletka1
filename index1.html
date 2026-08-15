from aiogram import Bot, Dispatcher, types
from aiohttp import web

bot = Bot(token="ВАШ_ТОКЕН_БОТА")
dp = Dispatcher()

# Обработчик запроса от вашего WebApp
async def create_invoice_handler(request):
    cost = int(request.rel_url.query.get('cost', 10))
    
    # Создаем инвойс на оплату Telegram Stars (валюта XTR)
    invoice_link = await bot.create_invoice_link(
        title=f"Прокрутка рулетки",
        description=f"Оплата за прокрутку рулетки ({cost} звезд)",
        payload=f"spin_{cost}",
        currency="XTR",
        prices=[types.LabeledPrice(label="Stars", amount=cost)]
    )
    
    return web.json_response({"invoice_link": invoice_link})

# Обязательный обработчик подтверждения платежа от Telegram
@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
