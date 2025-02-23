from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums.parse_mode import ParseMode
import asyncio

from buttons.keyboards import admin_kb
from config import admin_id
from db.database import get_db
from db.services import get_all_users

router = Router()

class AdminStates(StatesGroup):
    waiting_for_broadcast = State()

# Простой фильтр для проверки, является ли пользователь администратором
async def is_admin_filter(message: types.Message):
    return str(message.from_user.id) == admin_id

@router.message(Command('admin'), is_admin_filter)
async def admin_panel(message: types.Message):
    await message.answer(
        "Добро пожаловать в панель администратора! 🎛️\n\n"
        "Здесь вы можете управлять ботом и пользователями.",
        reply_markup=admin_kb
    )

@router.message(F.text == "📊 Статистика пользователей", is_admin_filter)
async def user_statistics(message: types.Message):
    with get_db() as db:
        users = get_all_users(db)
        total_users = len(users)
        
        stats = f"📊 <b>Статистика бота</b>\n\n"
        stats += f"👥 Всего пользователей: {total_users}\n"
        
        await message.answer(stats, parse_mode=ParseMode.HTML.value)

@router.message(F.text == "📨 Рассылка сообщений", is_admin_filter)
async def start_broadcast(message: types.Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, отправьте сообщение для рассылки всем пользователям.\n"
        "Сообщение может содержать текст, фото или видео."
    )
    await state.set_state(AdminStates.waiting_for_broadcast)

@router.message(AdminStates.waiting_for_broadcast, is_admin_filter)
async def process_broadcast(message: types.Message, state: FSMContext):
    with get_db() as db:
        users = get_all_users(db)
        sent_count = 0
        failed_count = 0

        await message.answer("Начинаем рассылку...")

        for user in users:
            try:
                await message.copy_to(user.telegram_id)
                sent_count += 1
                await asyncio.sleep(0.1)  # Prevent flooding
            except Exception as e:
                failed_count += 1

        summary = f"📨 <b>Итоги рассылки</b>\n\n"
        summary += f"✅ Успешно отправлено: {sent_count}\n"
        summary += f"❌ Не удалось отправить: {failed_count}"

        await message.answer(summary, parse_mode=ParseMode.HTML)
        await state.clear()

@router.message(F.text == "🔄 Состояние системы", is_admin_filter)
async def system_status(message: types.Message):

    import psutil
    import datetime

    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())

    status = f"🖥️ <b>Состояние системы</b>\n\n"
    status += f"Загрузка ЦП: {cpu_percent}%\n"
    status += f"Использование памяти: {memory.percent}%\n"
    status += f"Использование диска: {disk.percent}%\n"
    status += f"Время работы: {str(uptime).split('.')[0]}"

    await message.answer(status, parse_mode=ParseMode.HTML)

@router.message(F.text == "⬅️ Вернуться в главное меню", is_admin_filter)
async def back_to_main_menu(message: types.Message):
    from buttons.keyboards import main_kb
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_kb)
