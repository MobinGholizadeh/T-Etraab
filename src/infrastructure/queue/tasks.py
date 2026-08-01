import logging
import asyncio
import os
import tempfile
import uuid
import json
import redis
from aiogram import Bot

from src.infrastructure.queue.celery_app import celery_app
from src.application.use_cases.extract_task import ExtractTaskUseCase
from src.infrastructure.speech.whisper_client import WhisperClient
from src.infrastructure.providers.plane_provider import PlaneProvider
from src.infrastructure.providers.mock_provider import MockProvider
from src.application.services.notification_service import NotificationService
from src.config.settings import settings

logger = logging.getLogger(__name__)

def run_async(coro):
    """Helper to run async code in Celery sync tasks"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError("Loop is closed")
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_voice_task(self, file_id: str, telegram_chat_id: int):
    """Downloads voice, transcribes it, and triggers extraction"""
    try:
        logger.info(f"Processing voice for chat #{telegram_chat_id}")
        
                                   
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        
        async def download_voice():
            fd, temp_path = tempfile.mkstemp(suffix=".ogg")
            os.close(fd)
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path, destination=temp_path)
            await bot.session.close()
            return temp_path
            
        local_file_path = run_async(download_voice())
        
        try:
                           
            whisper = WhisperClient()
            persian_text = run_async(whisper.transcribe(local_file_path))
        finally:
                                          
            if os.path.exists(local_file_path):
                os.remove(local_file_path)
        
                                      
        process_text_task.delay(persian_text, telegram_chat_id)
        
    except Exception as exc:
        logger.error(f"Failed to process voice task: {exc}")
        self.retry(exc=exc)

@celery_app.task(bind=True, max_retries=3)
def process_text_task(self, persian_text: str, telegram_chat_id: int):
    """Runs Gemini extraction and translates to English"""
    try:
        logger.info(f"Processing text for chat #{telegram_chat_id}")
        
        use_case = ExtractTaskUseCase()
        extracted_data = run_async(use_case.execute(persian_text))
        
        # Store in Redis and wait for approval
        task_id = str(uuid.uuid4())
        redis_client = redis.Redis.from_url(settings.celery_broker_url)
        def json_serial(obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")
            
        redis_client.setex(f"task_pending:{task_id}", 86400, json.dumps(extracted_data, default=json_serial))
        
        notifier = NotificationService()
        run_async(notifier.ask_manager_approval(telegram_chat_id, extracted_data, task_id))
        
    except Exception as exc:
        logger.error(f"Failed to process text task: {exc}")
        self.retry(exc=exc)

@celery_app.task(bind=True, max_retries=3)
def create_provider_task(self, telegram_chat_id: int, extracted_data: dict):
    """Calls the task provider (Plane/Linear) to create the ticket"""
    try:
        logger.info(f"Creating task in provider for chat #{telegram_chat_id}")
        
        provider = PlaneProvider() if settings.ACTIVE_PROVIDER == "plane" else MockProvider()
        
                                                                                
                                                                                       
        assignee = extracted_data.get("assignedDeveloper")
        
        result = run_async(provider.create_task(
            title=extracted_data.get("englishTitle"),
            description=extracted_data.get("englishDescription"),
            project_id=None,                             
            assignee_id=assignee,                   
            priority=extracted_data.get("priority"),
            due_date=extracted_data.get("deadline"),
            labels=extracted_data.get("labels", [])
        ))
        
        # 3. Send Notification to Manager
        notifier = NotificationService()
        run_async(notifier.notify_manager(
            telegram_id=telegram_chat_id,
            task_title=extracted_data.get("englishTitle"),
            task_url=result.provider_task_url,
            developer_name=assignee or "Unassigned"
        ))
        
        # 4. Notify Developer if found
        if assignee:
            dev_name_lower = assignee.lower()
            dev_telegram_id = settings.DEV_TELEGRAM_IDS.get(dev_name_lower)
            if dev_telegram_id:
                logger.info(f"Notifying developer '{assignee}' at Telegram ID {dev_telegram_id}")
                run_async(notifier.notify_developer(
                    telegram_id=dev_telegram_id,
                    task_title=extracted_data.get("englishTitle"),
                    task_url=result.provider_task_url,
                    priority=extracted_data.get("priority"),
                    deadline=str(extracted_data.get("deadline")) if extracted_data.get("deadline") else None
                ))
            else:
                logger.warning(f"Developer '{assignee}' not found in DEV_TELEGRAM_IDS setting")
        
    except Exception as exc:
        logger.error(f"Failed to create provider task: {exc}")
        self.retry(exc=exc)
