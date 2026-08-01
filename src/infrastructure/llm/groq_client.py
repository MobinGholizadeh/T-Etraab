import logging
import json
from datetime import datetime
from groq import AsyncGroq
from typing import Dict, Any

from src.config.settings import settings
from src.core.exceptions import AIExtractionError

logger = logging.getLogger(__name__)

class GroqTaskExtractor:
    """Client for extracting structured task JSON from Persian text using Groq APIs"""
    
    def __init__(self):
        if settings.GROQ_API_KEY and "MOCK" not in settings.GROQ_API_KEY:
            self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
            self.model = "llama-3.3-70b-versatile"
        else:
            self.client = None

    async def extract_task(self, persian_text: str) -> Dict[str, Any]:
        """
        Extracts structured data from Persian text.
        Returns a dictionary that matches the AIExtractionSchema.
        """
        logger.info("Extracting task details using Groq")
        
        if not self.client:
                                         
            return {
                "confidence": 0.96,
                "title": "آپدیت بخش RCC",
                "description": "لطفا بخش RCC رو تا آخر هفته آپدیت کنید.",
                "originalTranscript": persian_text,
                "assignedDeveloper": "مبین",
                "priority": "High",
                "deadline": "2026-08-01",
                "estimatedDays": 4,
                "labels": ["Frontend", "React", "RCC"],
                "subtasks": ["Check API", "Update UI"],
                "acceptanceCriteria": ["No errors in console"],
                "questions": []
            }

        prompt = f"""
        You are an expert technical project manager and software architect.
        I will provide you with a Persian text or voice transcript from a manager.
        
        Your task is to extract structured task information from it.
        
        CRITICAL RULES:
        1. UNDERSTAND TIME IN PERSIAN: Evaluate expressions like "فردا" (tomorrow), "هفته آینده" (next week), "تا آخر هفته" (by weekend) and calculate the absolute deadline based on today. Today's date is {datetime.now().strftime('%Y-%m-%d')}.
        2. DETECT PRIORITY IN PERSIAN: "فوری", "اورژانسی", "خیلی مهم" -> Urgent/High. "اگه وقت شد", "بعدا" -> Low.
        3. EXTRACT WITHOUT TRANSLATION: Do not translate the title or description into English in this step. Keep them in Persian.
        4. ACCURACY: If the request is unclear, missing critical info, or ambiguous, return a lower `confidence` score (e.g., < 0.85) and add questions to the `questions` array.
        5. DO NOT HALLUCINATE: If a deadline, assignee, or priority is not mentioned, leave it null.
        6. ASSIGNEE MAPPING: You MUST map Persian names to standard usernames for assignees:
           - If you see "علی", "علی جان", "آقای همت نیا", or "علی آقا", output exactly "ali.hemmatnia"
           - If you see "مبین", "مبین جان", "آقای قلی زاده", or "آقا مبین", output exactly "mobingholizadeh10"
        
        Output MUST be valid JSON exactly matching this schema:
        {{
            "confidence": float (0.0 to 1.0),
            "title": "string",
            "description": "string",
            "originalTranscript": "string",
            "assignedDeveloper": "string or null",
            "priority": "string (Low/Medium/High/Urgent) or null",
            "deadline": "string YYYY-MM-DD or null",
            "estimatedDays": integer or null,
            "labels": ["string"],
            "subtasks": ["string"],
            "acceptanceCriteria": ["string"],
            "questions": ["string"]
        }}
        
        Text to analyze:
        {persian_text}
        """
        
        try:
            response = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that outputs only JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                response_format={"type": "json_object"},
            )
            
            result_json = response.choices[0].message.content
            return json.loads(result_json)
            
        except Exception as e:
            logger.error(f"Groq extraction failed: {e}")
            raise AIExtractionError(f"Failed to extract JSON from Groq: {str(e)}")
