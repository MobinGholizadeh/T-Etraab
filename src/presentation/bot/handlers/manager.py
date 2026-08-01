import logging
import json
import redis
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.infrastructure.queue.tasks import process_voice_task, process_text_task, create_provider_task
from src.config.settings import settings

logger = logging.getLogger(__name__)
router = Router(name="manager")

@router.message(Command("new"))
async def cmd_new(message: Message):
    await message.answer("Please send me a voice message or text describing the task in Persian.")

@router.message(F.voice)
async def handle_voice(message: Message):
    """Handle incoming voice messages from managers."""
    msg = await message.answer("🎙️ Voice message received. Downloading and transcribing...")
    
    file_id = message.voice.file_id
    
                                                                  
    process_voice_task.delay(file_id, message.chat.id)
    
    logger.info(f"Received voice message from chat {message.chat.id}, file: {file_id}")
    await msg.edit_text("⏳ Voice message is in the processing queue. I will notify you once the ticket is created.")

@router.message(F.text & ~F.text.startswith('/'))
async def handle_text_task(message: Message):
    """Handle incoming text messages from managers."""
    msg = await message.answer("📝 Text message received. Extracting task details...")
    
                                                                  
    process_text_task.delay(message.text, message.chat.id)
    
    logger.info(f"Received text task from chat {message.chat.id}")
    await msg.edit_text("⏳ Task extraction is in progress...")

@router.callback_query(F.data.startswith("approve_fa:") | F.data.startswith("approve_en:"))
async def handle_task_approval(callback: CallbackQuery):
    """Handle task approval from the manager"""
    action, task_id = callback.data.split(":")
    redis_client = redis.Redis.from_url(settings.celery_broker_url)
    
    # Retrieve pending task
    data = redis_client.get(f"task_pending:{task_id}")
    if not data:
        await callback.message.edit_text("❌ Task approval expired or already processed.")
        await callback.answer()
        return
        
    extracted_data = json.loads(data)
    
    # Delete from Redis
    redis_client.delete(f"task_pending:{task_id}")
    
    if action == "approve_fa":
        # Override the English translation with the raw Persian text
        extracted_data["englishTitle"] = extracted_data.get("title", "")
        extracted_data["englishDescription"] = extracted_data.get("description", "")
        lang_str = "Persian"
    else:
        lang_str = "English"
    
    # Queue task creation
    create_provider_task.delay(callback.message.chat.id, extracted_data)
    
    # Update message
    await callback.message.edit_text(
        f"{callback.message.html_text}\n\n✅ <b>Status:</b> Approved in {lang_str}. Creating task...",
        parse_mode="HTML"
    )
    await callback.answer(f"Task approved in {lang_str}!")

@router.callback_query(F.data.startswith("cancel:"))
async def handle_task_cancellation(callback: CallbackQuery):
    """Handle task cancellation from the manager"""
    task_id = callback.data.split(":")[1]
    redis_client = redis.Redis.from_url(settings.celery_broker_url)
    
    # Delete from Redis
    redis_client.delete(f"task_pending:{task_id}")
    
    # Update message
    await callback.message.edit_text(
        f"{callback.message.html_text}\n\n❌ <b>Status:</b> Cancelled.",
        parse_mode="HTML"
    )
    await callback.answer("Task creation cancelled.")
