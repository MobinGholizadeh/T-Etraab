from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass

@dataclass
class ProviderTaskResult:
    provider_task_id: str
    provider_task_url: str

class ITaskProvider(ABC):
    """Abstract interface for all task providers (Plane, Linear, etc.)"""
    
    @abstractmethod
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
        """Create a new task/issue in the external provider"""
        pass
    
    @abstractmethod
    async def get_user_id(self, email_or_name: str) -> Optional[str]:
        """Resolve a user identifier in the external provider"""
        pass
