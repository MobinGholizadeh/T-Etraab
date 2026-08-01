import logging
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.config.settings import settings

logger = logging.getLogger(__name__)

class NotificationService:
    """Service to send notifications via Telegram"""
    
    def __init__(self):
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        
    async def notify_manager(self, telegram_id: int, task_title: str, task_url: str, developer_name: str = "Unassigned"):
        """Notify the manager that their task was successfully created"""
        message = (
            f"✅ <b>Task Created Successfully!</b>\n\n"
            f"<b>Title:</b> {task_title}\n"
            f"<b>Assigned to:</b> {developer_name}\n\n"
            f"<a href='{task_url}'>View Task</a>"
        )
        try:
            await self.bot.send_message(chat_id=telegram_id, text=message, parse_mode="HTML")
            logger.info(f"Notified manager {telegram_id} about task creation.")
        except Exception as e:
            logger.error(f"Failed to notify manager {telegram_id}: {e}")
            
    async def notify_developer(self, telegram_id: int, task_title: str, task_url: str, priority: str, deadline: str):
        """Notify the developer that a new task was assigned to them"""
        message = (
            f"🔔 <b>New Task Assigned to You!</b>\n\n"
            f"<b>Title:</b> {task_title}\n"
            f"<b>Priority:</b> {priority or 'Normal'}\n"
            f"<b>Deadline:</b> {deadline or 'None'}\n\n"
            f"<a href='{task_url}'>View Task</a>"
        )
        try:
            await self.bot.send_message(chat_id=telegram_id, text=message, parse_mode="HTML")
            logger.info(f"Notified developer {telegram_id} about task assignment.")
        except Exception as e:
            logger.error(f"Failed to notify developer {telegram_id}: {e}")

    async def ask_manager_approval(self, telegram_id: int, extracted_data: dict, task_id: str):
        """Ask manager to approve the extracted task details before creation"""
        message = (
            f"🔍 <b>Please review the extracted task:</b>\n\n"
            f"<b>Title (English):</b> {extracted_data.get('englishTitle', 'N/A')}\n"
            f"<b>Description (English):</b> {extracted_data.get('englishDescription', 'N/A')}\n\n"
            f"<b>Title (Persian):</b> {extracted_data.get('title', 'N/A')}\n"
            f"<b>Description (Persian):</b> {extracted_data.get('description', 'N/A')}\n\n"
            f"<b>Assigned to:</b> {extracted_data.get('assignedDeveloper', 'Unassigned')}\n"
            f"<b>Priority:</b> {extracted_data.get('priority', 'Normal')}\n"
            f"<b>Deadline:</b> {extracted_data.get('deadline', 'None')}\n"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🇮🇷 Approve in Persian", callback_data=f"approve_fa:{task_id}"),
                InlineKeyboardButton(text="🇬🇧 Approve in English", callback_data=f"approve_en:{task_id}")
            ],
            [
                InlineKeyboardButton(text="❌ Cancel", callback_data=f"cancel:{task_id}")
            ]
        ])
        
        try:
            await self.bot.send_message(chat_id=telegram_id, text=message, reply_markup=keyboard, parse_mode="HTML")
            logger.info(f"Requested approval from manager {telegram_id} for task {task_id}.")
        except Exception as e:
            logger.error(f"Failed to ask approval from manager {telegram_id}: {e}")
