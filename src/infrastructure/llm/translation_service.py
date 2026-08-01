import logging
from groq import AsyncGroq

from src.config.settings import settings

logger = logging.getLogger(__name__)

class GroqTranslator:
    """Client for translating Persian task titles and descriptions to Professional English using Groq"""
    
    def __init__(self):
        if settings.GROQ_API_KEY and "MOCK" not in settings.GROQ_API_KEY:
            self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
            self.model = "llama-3.1-8b-instant"                             
        else:
            self.client = None

    async def translate_to_english(self, title: str, description: str) -> tuple[str, str]:
        """
        Translates Persian title and description to professional English.
        Returns (english_title, english_description)
        """
        logger.info("Translating task to English with Groq")
        
        if not self.client:
            return ("Update RCC section", "Please update the RCC section by the end of the week.")

        prompt = f"""
        Translate the following task title and description from Persian to Professional Software Engineering English.
        
        CRITICAL RULES:
        1. NEVER translate Code, Component names, API names, Database tables, Framework names, or File names.
        2. Keep technical terms intact (e.g. RCC, API, DB).
        3. Make the tone professional and clear, suitable for a Jira/Plane/Linear ticket.
        
        Title: {title}
        Description: {description}
        
        Output format: 
        Title: <english_title>
        Description: <english_description>
        """
        
        try:
            response = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
            )
            
            text = response.choices[0].message.content
            
                          
            eng_title = ""
            eng_desc = ""
            for line in text.split("\n"):
                if line.startswith("Title:"):
                    eng_title = line.replace("Title:", "").strip()
                elif line.startswith("Description:"):
                    eng_desc = line.replace("Description:", "").strip()
            
                                     
            if not eng_title:
                eng_title = text.split("\n")[0]
                
            return eng_title, eng_desc
            
        except Exception as e:
            logger.error(f"Translation failed via Groq: {e}")
                                                      
            return title, description
