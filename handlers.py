# bot/handlers/user/start.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from keyboards.reply import get_main_menu
from state import DomainState


router = Router()
@router.message(F.text == 'New chat')
async def new_chat(message:Message, state:FSMContext):

    await message.answer("Выберете область о которой хотите узнать")
    await state.set_state(DomainState.domain)



@router.message(Command("start"))
async def cmd_start(message: Message, state:FSMContext):
  

    await message.answer(
        f"👋 Здравствуйте, {message.from_user.full_name}!\n"
        "Добро пожаловать в это бот с искуственным интелектом\n" \
        "Выберете область о которой хотите узнать",
        # "Выберите действие:",
        reply_markup=get_main_menu()
    )
    await state.set_state(DomainState.domain)


@router.message(DomainState.query)
async def process_name(message: Message, state: FSMContext):
    from chat import final_chain
    DEFAULT_SESSION_ID = '1'
    data = await state.get_data()
    
    answer = final_chain.invoke({"domain": data["domain"], "question": message.text},
            config={"configurable": {"session_id": DEFAULT_SESSION_ID}},)
    await message.answer(answer)


@router.message(DomainState.domain)
async def start_domain(message: Message, state: FSMContext):
    await state.update_data(domain=message.text)
    await message.answer("👤 Введите ваш запрос:", reply_markup=get_main_menu())
    await state.set_state(DomainState.query)








# @router.message()
# async def query(message:Message):
   

#     domain = message.text

#     answer = final_chain.invoke({"domain": domain, "question": user_question},
#             config={"configurable": {"session_id": DEFAULT_SESSION_ID}},)


#     return await message.answer(query)

# @router.message(F.text == "📂 Каталог")
# async def show_catalog(message: Message, session: AsyncSession):
#     from models.category import Category
#     categories = (await session.scalars(select(Category))).all()
#     if not categories:
#         await message.answer("К сожалению, категории пока не добавлены.")
#         return
#     await message.answer("📂 Выберите категорию:", reply_markup=categories_kb(categories))

# # bot/handlers/user/start.py — ЗАМЕНИ ФУНКЦИЮ view_cart НА ЭТУ:

# @router.message(F.text == "🛒 Корзина")
# async def view_cart(message: Message, session: AsyncSession):
#     # Получаем telegram_id пользователя
#     user_tg_id = message.from_user.id

#     # Находим пользователя в БД
#     from models.user import User
#     user = (await session.scalars(select(User).where(User.telegram_id == user_tg_id))).first()
#     if not user:
#         await message.answer("❌ Сначала начните диалог с ботом через /start.")
#         return

#     # Получаем товары в корзине
#     from models.cart import CartItem
#     cart_items = (await session.scalars(
#         select(CartItem).where(CartItem.user_id == user.id).options(selectinload(CartItem.product))
#     )).all()

#     if not cart_items:
#         await message.answer("🛒 Ваша корзина пуста.")
#         return

#     total = sum(item.quantity * item.product.price for item in cart_items)
#     text = "🛒 <b>Ваша корзина</b>:\n\n"
#     for item in cart_items:
#         text += f"▪️ {item.product.name}\n  {item.quantity} × {item.product.price} = <b>{item.quantity * item.product.price} руб.</b>\n"

#     text += f"\n<b>Итого: {total} руб.</b>"

#     from keyboards.inline import cart_kb
#     await message.answer(text, reply_markup=cart_kb(cart_items), parse_mode="HTML")

# @router.message(F.text == "🛠 Админка")
# async def show_admin_panel(message: Message, session: AsyncSession):
#     from config import settings
#     if message.from_user.id not in settings.ADMIN_IDS:
#         await message.answer("🚫 У вас нет доступа к админке.")
#         return

#     from keyboards.inline import admin_kb
#     await message.answer("🛠 Панель администратора:", reply_markup=admin_kb())