from aiogram import Router, F, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from chatgpt_md_converter import telegram_format

from buttons.keyboards import main_kb, tools_kb
from db.database import get_db
from db.services import get_or_create_user
from heandlers.code_review_handler import CodeReview


router = Router()

class HomeworkHelp(StatesGroup):
    waiting_for_task = State()

@router.message(Command("start"))
async def start_cmd(message: Message):
    with get_db() as db:
        user = get_or_create_user(
            db,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
    
    welcome_text = '''<b>Привет! Я Code Review Bot 🤖</b>
Я помогу тебе с:

✅ Проверкой кода
📚 Домашними заданиями
💻 Другими инструментами разработки

🔍 Поиск ошибок <code>(Error Detection)</code> – найду синтаксические и логические ошибки
⚡ Оптимизация кода <code>(Code Optimization)</code> – подскажу, как сделать код быстрее и эффективнее
📖 Генерация документации <code>(Documentation Generation)</code> – помогу оформить документацию
🔎 Объяснение кода <code>(Code Explanation)</code> – разберу код и объясню, как он работает
🧪 Генерация тестов <code>(Test Generation)</code> – создам автоматические тесты

Отправьте /review, чтобы начать проверку кода! 🚀
Или выберите нужную опцию в меню ниже 👇"""'''

    
    await message.answer(text=welcome_text, reply_markup=main_kb, parse_mode=ParseMode.HTML.value)

@router.message(F.text == "🔍 Проверка кода")
async def code_review(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте ваш код для проверки.")
    await state.set_state(CodeReview.waiting_for_code)

@router.message(F.text == "📚 Помощь с домашним заданием")
async def homework_help(message: Message, state: FSMContext):
    await message.answer("Опишите ваше задание, и я помогу вам его решить.")
    await state.set_state(HomeworkHelp.waiting_for_task)

@router.message(HomeworkHelp.waiting_for_task)
async def process_homework(message: Message, state: FSMContext):
    await message.bot.send_chat_action(message.chat.id, 'typing')
    with get_db() as db:
        user = get_or_create_user(
            db,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        
        prompt = [
            {"role": "system", "content": "Вы - полезный преподаватель-ассистент. Помогите студенту понять и решить его домашнее задание. Предоставляйте объяснения и рекомендации, а не просто решение."},
            {"role": "user", "content": message.text}
        ]
        
        from api.openai import ask_ai
        response = ask_ai(prompt)
        await message.answer(telegram_format(response), parse_mode=ParseMode.HTML.value)
        await state.clear()

@router.message(F.text == "💻 Другие инструменты")
async def other_tools(message: Message):
    await message.answer("Выберите инструмент:", reply_markup=tools_kb)

@router.message(F.text == "❓ Помощь")
async def help_command(message: Message):
    help_text = """🤖 Как использовать бота:

1️⃣ Проверка кода - отправьте свой код для анализа
2️⃣ Помощь с домашним заданием - опишите задание
3️⃣ Другие инструменты - форматирование, поиск ошибок и документация

Если у вас есть вопросы, не стесняйтесь спрашивать!"""
    await message.answer(help_text)

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.answer("Главное меню:", reply_markup=main_kb)
    await callback.message.delete()
    await callback.answer()