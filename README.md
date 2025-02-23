# Code Review Bot 🤖

A powerful Telegram bot designed to help developers with code review, homework assistance, and various development tools.

## Features ✨

- ✅ **Code Review** - Get detailed code analysis and improvement suggestions
- 📚 **Homework Help** - Get assistance with programming assignments
- 🔍 **Error Detection** - Find syntax and logical errors in your code
- ⚡ **Code Optimization** - Get suggestions for improving code performance
- 📖 **Documentation Generation** - Generate code documentation
- 🔎 **Code Explanation** - Get detailed explanations of how code works
- 🧪 **Test Generation** - Generate automated tests for your code

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/bekjonbegmatov/Review-TG.git
cd Review-TG
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
venv\Scripts\activate    # For Windows
```

3. Install required packages:
```bash
pip install -r moduls.txt
```

## Environment Setup 🔑

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Configure the following environment variables in `.env`:
```env
BOT_TOCEN="your_telegram_bot_token"  # Get from @BotFather
OPEN_AI_API_KEY="your_openai_api_key"  # Get from platform.openai.com
ADMIN_ID="your_telegram_id"  # Get from @my_idbot
```

## Running the Bot 🏃‍♂️

1. Start the bot:
```bash
python main.py
```

## Usage 📝

### Available Commands

- `/start` - Start the bot and see the main menu
- `/review` - Start a code review session
- `/stop` - End the current code review session
- `/history` - View your code review history
- `/help` - Get help with bot usage

### Tools

1. **Code Review**
   - Send your code to get comprehensive feedback
   - Receive suggestions for improvements
   - Get insights about best practices

2. **Homework Help**
   - Get assistance with programming assignments
   - Receive explanations and guidance

3. **Development Tools**
   - Error Detection
   - Code Optimization
   - Documentation Generation
   - Code Explanation
   - Test Generation

## Data Storage 💾

The bot utilizes SQLite database for efficient data management:

- **User Data Storage**
  - User profiles and preferences

- **Code Review History**
  - Previous code submissions
  - Review comments and suggestions

## Admin Panel 👨‍💼

The bot includes a comprehensive admin panel with the following features:

1. **User Management**
   - View all registered users
   - Manage user permissions

2. **Broadcast Messaging**
   - Send announcements to all users