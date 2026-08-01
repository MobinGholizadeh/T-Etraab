import logging
import httpx
from src.config.settings import settings
from src.core.exceptions import AudioProcessingError

logger = logging.getLogger(__name__)

class WhisperClient:
    """Client for converting speech to text using Groq Whisper"""
    
    def __init__(self, api_key: str = None):
                                                         
        self.api_key = api_key or settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1/audio/transcriptions"
        
    async def transcribe(self, file_path: str) -> str:
        """
        Takes an audio file and transcribes it using Whisper.
        Returns the transcribed text.
        """
        logger.info(f"Transcribing audio file: {file_path}")
        
                                                          
        if not self.api_key or "MOCK" in self.api_key:
            return "فردا تا آخر وقت باید بخش RCC رو آپدیت کنی، به مبین هم بگو کمک کنه، خیلی فوریه."

        try:
            async with httpx.AsyncClient() as client:
                with open(file_path, "rb") as f:
                    files = {"file": f}
                    data = {"model": "whisper-large-v3", "language": "fa"}                  
                    headers = {"Authorization": f"Bearer {self.api_key}"}
                    
                    response = await client.post(
                        self.base_url,
                        files=files,
                        data=data,
                        headers=headers,
                        timeout=60.0
                    )
                    
                    response.raise_for_status()
                    result = response.json()
                    return result.get("text", "")
                    
        except Exception as e:
            logger.error(f"Failed to transcribe audio: {e}")
            raise AudioProcessingError(f"Whisper transcription failed: {str(e)}")
