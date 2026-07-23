from app.exceptions.base import EKIPError


class LLMError(EKIPError):
    """
    Raised when an LLM operation fails.
    """