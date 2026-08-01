import logging
from typing import Dict, Any

from src.infrastructure.llm.groq_client import GroqTaskExtractor
from src.infrastructure.llm.translation_service import GroqTranslator
from src.domain.schemas.extraction import AIExtractionSchema
from src.core.exceptions import LowConfidenceError

logger = logging.getLogger(__name__)

class ExtractTaskUseCase:
    """Orchestrates AI extraction, validation, and translation."""
    
    def __init__(self):
        self.extractor = GroqTaskExtractor()
        self.translator = GroqTranslator()
        
    async def execute(self, persian_text: str, confidence_threshold: float = 0.85) -> Dict[str, Any]:
        """
        1. Extracts JSON
        2. Validates against Schema
        3. Checks Confidence
        4. Translates if confidence is high enough
        """
                         
        raw_json = await self.extractor.extract_task(persian_text)
        
                                    
                                                                              
        validated_data = AIExtractionSchema(**raw_json)
        
                             
        if validated_data.confidence < confidence_threshold:
            logger.warning(f"Low confidence task extraction: {validated_data.confidence}")
            raise LowConfidenceError("AI could not understand the request with enough confidence.")
            
                                            
        eng_title, eng_desc = await self.translator.translate_to_english(
            validated_data.title, 
            validated_data.description
        )
        
                                                     
        final_data = validated_data.model_dump()
        final_data["englishTitle"] = eng_title
        final_data["englishDescription"] = eng_desc
        
        return final_data
