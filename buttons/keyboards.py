from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Main menu keyboard
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Проверка кода")],
        [KeyboardButton(text="📚 Помощь с домашним заданием")],
        [KeyboardButton(text="💻 Другие инструменты")],
        [KeyboardButton(text="❓ Помощь")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

# Other tools keyboard
tools_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Поиск ошибок", callback_data="find_bugs")],
        [InlineKeyboardButton(text="⚡ Оптимизация кода", callback_data="optimize_code")],
        [InlineKeyboardButton(text="📖 Генерация документации", callback_data="generate_docs")],
        [InlineKeyboardButton(text="🔎 Объяснение кода", callback_data="explain_code")],
        [InlineKeyboardButton(text="🧪 Генерация тестов", callback_data="generate_tests")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
    ]
)

# Admin panel keyboard
admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📨 Рассылка сообщений")],
        [KeyboardButton(text="📊 Статистика пользователей")],
        [KeyboardButton(text="🔄 Состояние системы")],
        [KeyboardButton(text="⬅️ Вернуться в главное меню")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие администратора"
)