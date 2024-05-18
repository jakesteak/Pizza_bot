from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f
from filters.chat_types import ChatTypeFilter
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from kbds.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет, я виртуальный помощник",
        reply_markup=get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            placeholder="Что Вас интересует?",
            sizes=(2, 2)
        )
    )


# @user_private_router.message(F.text.lower() == 'меню')
@user_private_router.message(or_f(Command("menu"), F.text.lower() == 'меню'))
@user_private_router.message(Command('menu'))
async def menu_cmd(message: types.Message):
    await message.answer("Вот меню:")


@user_private_router.message(F.text.lower() == 'о магазине')
@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer("О магазине:")


@user_private_router.message(F.text.lower() == 'варианты оплаты')
@user_private_router.message(Command('payment'))
async def payment_cmd(message: types.Message):
    text = as_marked_section(
            Bold("Варианты оплаты:"),
            "Картой в боте",
            "При получении картой/наличными",
            "В заведении",
            marker='✅ '
        )
    await message.answer(text.as_html())


@user_private_router.message((F.text.lower().contains('доставк')) | (F.text.lower() == 'варианты доставки'))
@user_private_router.message(Command('shipping'))
async def shipping_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
        Bold("Варианты доставки:"),
        "Курьер",
        "Самовынос (сейчас прибегу заберу)",
        "Покушаю у Вас (сейчас прибегу)",
        marker='✅ '
        ),
        as_marked_section(
        Bold("Нельзя:"),
        "Почта",
        "Голуби",
        marker='❌ '
        ),
        sep='\n---------------------------------------------------------------\n'
    )
    await message.answer(text.as_html())


@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(f"номер получен")
    await message.answer(str(message.contact))


@user_private_router.message(F.location)
async def get_location(message: types.Message):
    await message.answer(f"локация получена")
    await message.answer(str(message.location))