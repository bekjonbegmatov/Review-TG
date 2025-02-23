from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Initialize configuration variables
bot_tocen = os.getenv('BOT_TOCEN1', '').strip()
open_ai_api_key = os.getenv('OPEN_AI_API_KEY1')
admin_id = os.getenv('ADMIN_ID1')

