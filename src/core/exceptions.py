class PlatformException(Exception):
    """Base exception for all custom platform exceptions"""
    pass

class AudioProcessingError(PlatformException):
    """Raised when there's an error downloading or transcribing audio"""
    pass

class AIExtractionError(PlatformException):
    """Raised when Gemini fails to extract valid JSON or encounters an API error"""
    pass

class LowConfidenceError(PlatformException):
    """Raised when the AI extraction confidence is below the required threshold"""
    pass

class ProviderError(PlatformException):
    """Raised when the Task Provider (Plane/Linear) returns an error"""
    pass
