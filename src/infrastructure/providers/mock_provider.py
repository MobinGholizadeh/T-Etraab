import logging
import uuid
from typing import Optional

from src.domain.interfaces.task_provider import ITaskProvider, ProviderTaskResult

logger = logging.getLogger(__name__)

class MockProvider(ITaskProvider):
    """Mock provider for testing the pipeline without external dependencies"""
    
    async def create_task(
        self,
        title: str,
        description: str,
        project_id: Optional[str],
        assignee_id: Optional[str],
        priority: Optional[str],
        due_date: Optional[str],
        labels: list[str]
    ) -> ProviderTaskResult:
        logger.info(f"MOCK PROVIDER: Creating task '{title}' assigned to {assignee_id}")
        
        task_id = f"MOCK-{str(uuid.uuid4())[:8]}"
        return ProviderTaskResult(
            provider_task_id=task_id,
            provider_task_url=f"https://mock.provider.local/tasks/{task_id}"
        )
        
    async def get_user_id(self, email_or_name: str) -> Optional[str]:
        logger.info(f"MOCK PROVIDER: Looking up user {email_or_name}")
        return f"mock_user_{email_or_name.lower().replace(' ', '_')}"
