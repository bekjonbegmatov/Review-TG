from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums.parse_mode import ParseMode  

from db.database import get_db
from db.services import (
    get_or_create_user,
    create_conversation,
    add_message,
    get_conversation_messages,
    get_user_conversations
)
from api.openai import ask_ai
from chatgpt_md_converter import telegram_format

router = Router()

class CodeReview(StatesGroup):
    waiting_for_code = State()
    in_conversation = State()

@router.message(Command('review'))
async def start_code_review(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, отправьте мне код, который вы хотите, чтобы я проверил. "
        "Я проанализирую его и предоставлю предложения по улучшению."
    )
    await state.set_state(CodeReview.waiting_for_code)

@router.message(Command('stop'))
async def stop_review(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state in [CodeReview.waiting_for_code.state, CodeReview.in_conversation.state]:
        await state.clear()
        await message.answer("Сессия проверки кода завершена. Используйте /review для начала новой проверки.")
    else:
        await message.answer("Нет активной сессии проверки кода.")

@router.message(CodeReview.waiting_for_code)
async def process_code(message: Message, state: FSMContext):
    try:
        await message.bot.send_chat_action(message.chat.id, 'typing')
        with get_db() as db:
            user = get_or_create_user(
                db,
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )

            conversation = create_conversation(db, user, title=f"Code Review {message.date}")
            await state.update_data(conversation_id=conversation.id)
            
            add_message(db, conversation.id, 'user', message.text)
            
            prompt = [
                {"role": "system", "content": f" {get_formater_prompt()}. Вы - полезный ассистент по проверке кода. Проанализируйте код и предоставьте конструктивную обратную связь, "
                                            "фокусируясь на: 1) Качестве кода 2) Лучших практиках 3) Потенциальных ошибках 4) Улучшении производительности "
                                            "5) Проблемах безопасности. Будьте конкретны и приводите примеры где это возможно."},
                {"role": "user", "content": message.text}
            ]
            
            response = ask_ai(prompt)
            add_message(db, conversation.id, 'assistant', response)
            
            # Send response to user
            await message.answer(telegram_format(response), parse_mode=ParseMode.HTML.value)
            await message.answer("Вы можете задать дополнительные вопросы по коду или отправить /stop для завершения сессии.")
            
            # Change state to in_conversation
            await state.set_state(CodeReview.in_conversation)
            
    except Exception as e:
        await message.answer(f"An error occurred while processing your code: {str(e)}")
        await state.clear()

@router.message(CodeReview.in_conversation)
async def continue_conversation(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        conversation_id = data.get('conversation_id')
        await message.bot.send_chat_action(message.chat.id, 'typing')
        
        with get_db() as db:
            add_message(db, conversation_id, 'user', message.text)
            
            messages = get_conversation_messages(db, conversation_id)
            prompt = [
                {"role": "system", "content": "Вы - полезный ассистент по проверке кода. Отвечайте на вопросы пользователя о коде, используя контекст предыдущего обсуждения."}
            ]
            
            for msg in messages:
                prompt.append({"role": msg['role'], "content": msg['content']})
            
            response = ask_ai(prompt)
            add_message(db, conversation_id, 'assistant', response)
    
            await message.answer(telegram_format(response), parse_mode=ParseMode.HTML)
            
    except Exception as e:
        await message.answer(f"An error occurred while processing your message: {str(e)}")

@router.message(Command('history'))
async def show_history(message: Message):
    try:
        await message.bot.send_chat_action(message.chat.id, 'typing')
        with get_db() as db:
            user = get_or_create_user(
                db,
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
            conversations = get_user_conversations(db, user.id)
            
            if not conversations:
                await message.answer("У вас пока нету истории проверки кода.")
                return
            
            history_text = "Ваша история :\n\n"
            for conv in conversations:
                history_text += f"📝 {conv.title}\n"
                messages = get_conversation_messages(db, conv.id)
                for msg in messages:
                    if msg['role'] == 'user':
                        history_text += f"👤 Ваш код:\n{msg['content'][:100]}...\n\n"
                    else:
                        history_text += f"🤖 Review:\n{msg['content'][:100]}...\n\n"
                history_text += "---\n"
            
            await message.answer(telegram_format(history_text), parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.answer(f"An error occurred while fetching your history: {str(e)}")
        
def get_formater_prompt():
    print('cal function')
    return '''используй пожалуйста эти теги для выявления и форматирования текста которые ты генерирует например что-то нужно выделить жирным Заверни их в тег <b>bold</b> И так далее со всеми форматированием не надо использовать другие только вот это используй и всё, <strong>bold</strong>
<i>italic</i>, <em>italic</em>
<u>underline</u>, <ins>underline</ins>
<s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
<span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler>
<b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b>
<a href="http://www.example.com/">inline URL</a>
<a href="tg://user?id=123456789">inline mention of a user</a>
<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>
<code>inline fixed-width code</code>
<pre>pre-formatted fixed-width code block</pre>
<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
<blockquote>Block quotation started\nBlock quotation continued\nThe last line of the block quotation</blockquote>
<blockquote expandable>Expandable block quotation started\nExpandable block quotation continued\nExpandable block quotation continued\nHidden by default part of the block quotation started\nExpandable block quotation continued\nThe last line of the block quotation</blockquote> '''