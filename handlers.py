# bot/handlers/user/start.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from keyboards.reply import get_main_menu
from state import DomainState
from utils import logger, get_redis_history


router = Router()


@router.message(F.text == "New chat")
async def new_chat(message: Message, state: FSMContext):
    redis = get_redis_history(session_id=str(message.from_user.id))
    redis.clear()

    await message.answer("Выберете область о которой хотите узнать")
    await state.set_state(DomainState.domain)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):

    await message.answer(
        f"👋 Здравствуйте, {message.from_user.full_name}!\n"
        "Добро пожаловать в это бот с искуственным интелектом\n"
        "Выберете область о которой хотите узнать",
        # "Выберите действие:",
        reply_markup=get_main_menu(),
    )
    await state.set_state(DomainState.domain)


@router.message(DomainState.query)
async def process_name(message: Message, state: FSMContext):
    from chat import final_chain

    session_id = str(message.from_user.id)
    data = await state.get_data()
    try:
        answer = final_chain.invoke(
            {"domain": data["domain"], "question": message.text},
            config={"configurable": {"session_id": session_id}},
        )

        await message.answer(answer)
    except Exception as e:
        logger.error(f"Ошибка при генерации ответа: {e}")
        await message.answer("⚠️ Произошла ошибка. Попробуйте позже.")


@router.message(DomainState.domain)
async def start_domain(message: Message, state: FSMContext):
    await state.update_data(domain=message.text)
    await message.answer("👤 Введите ваш запрос:", reply_markup=get_main_menu())
    await state.set_state(DomainState.query)




@router.message()
async def err_handler(message:Message, state: FSMContext):
    await message.answer(
        f"👋 Здравствуйте, {message.from_user.full_name}!\n"
        "Добро пожаловать в это бот с искуственным интелектом\n"
        "Выберете область о которой хотите узнать",
        # "Выберите действие:",
        reply_markup=get_main_menu(),
    )
    await state.set_state(DomainState.domain)