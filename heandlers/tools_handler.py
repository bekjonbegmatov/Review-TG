from aiogram import Router, F, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from db.database import get_db
from db.services import get_or_create_user
from api.openai import ask_ai

from chatgpt_md_converter import telegram_format

router = Router()

class ToolsState(StatesGroup):
    waiting_for_code = State()

@router.callback_query(F.data == "find_bugs")
async def find_bugs(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Пожалуйста, отправьте код для проверки на ошибки. "
        "Я проанализирую его с помощью статического анализа."
    )
    await state.set_state(ToolsState.waiting_for_code)
    await state.update_data(tool_type="find_bugs")
    await callback.answer()

@router.callback_query(F.data == "optimize_code")
async def optimize_code(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Пожалуйста, отправьте код для оптимизации. "
        "Я проанализирую его и предложу улучшения производительности."
    )
    await state.set_state(ToolsState.waiting_for_code)
    await state.update_data(tool_type="optimize_code")
    await callback.answer()

@router.callback_query(F.data == "generate_docs")
async def generate_docs(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Пожалуйста, отправьте код для генерации документации. "
        "Я создам подробное описание и комментарии."
    )
    await state.set_state(ToolsState.waiting_for_code)
    await state.update_data(tool_type="generate_docs")
    await callback.answer()

@router.callback_query(F.data == "explain_code")
async def explain_code(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Пожалуйста, отправьте код для объяснения. "
        "Я проанализирую его и объясню, что он делает."
    )
    await state.set_state(ToolsState.waiting_for_code)
    await state.update_data(tool_type="explain_code")
    await callback.answer()

@router.callback_query(F.data == "generate_tests")
async def generate_tests(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Пожалуйста, отправьте код для генерации тестов. "
        "Я создам unit-тесты для вашего кода."
    )
    await state.set_state(ToolsState.waiting_for_code)
    await state.update_data(tool_type="generate_tests")
    await callback.answer()

@router.message(ToolsState.waiting_for_code)
async def process_code(message: types.Message, state: FSMContext):
    await message.bot.send_chat_action(message.chat.id, 'typing')
    data = await state.get_data()
    tool_type = data.get('tool_type')

    try:
        with get_db() as db:
            user = get_or_create_user(
                db,
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )

            prompts = {
                "find_bugs": "Вы - эксперт по анализу кода. Проведите статический анализ кода, найдите синтаксические ошибки, потенциальные баги, нарушения стиля кодирования и проблемы безопасности. Используйте подход, аналогичный инструментам flake8 и pylint. Предоставьте подробный отчет с указанием строк кода и рекомендациями по исправлению.",
                "optimize_code": "Вы - эксперт по оптимизации кода. Проанализируйте код на предмет производительности. Найдите места, где можно улучшить скорость выполнения, уменьшить использование памяти или улучшить алгоритмическую сложность. Предложите конкретные улучшения с примерами кода.",
                "generate_docs": "Вы - эксперт по документированию кода. Создайте подробную документацию для предоставленного кода. Включите описание функций, классов, параметров, возвращаемых значений и примеры использования. Следуйте лучшим практикам документирования кода.",
                "explain_code": "Вы - преподаватель программирования. Объясните, что делает предоставленный код, как он работает и какова его цель. Разбейте объяснение на логические части и используйте понятные примеры.",
                "generate_tests": "Вы - эксперт по тестированию. Создайте набор unit-тестов для предоставленного кода. Включите тесты на основные функции, граничные случаи и обработку ошибок. Используйте популярные фреймворки для тестирования."
            }

            prompt = [
                {"role": "system", "content": prompts[tool_type]},
                {"role": "user", "content": message.text}
            ]

            response = ask_ai(prompt)
            await message.answer(telegram_format(response), parse_mode=ParseMode.HTML)
            await state.clear()

    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке кода: {str(e)}")
        await state.clear()