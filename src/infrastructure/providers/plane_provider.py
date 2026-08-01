import logging
import httpx
from typing import Optional

from src.domain.interfaces.task_provider import ITaskProvider, ProviderTaskResult
from src.config.settings import settings
from src.core.exceptions import ProviderError

logger = logging.getLogger(__name__)

class PlaneProvider(ITaskProvider):
    """Integration with Plane.so API"""
    
    def __init__(self):
        self.api_key = settings.PLANE_API_KEY
        self.workspace_slug = settings.PLANE_WORKSPACE_SLUG
        self.base_url = "https://api.plane.so/api/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self._members_cache = None
        
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
        
        project = project_id or settings.PLANE_PROJECT_ID
        if not project or not self.workspace_slug:
            raise ProviderError("Plane Project ID or Workspace Slug is not configured.")
            
        url = f"{self.base_url}/workspaces/{self.workspace_slug}/projects/{project}/issues/"
        
                                                            
                                                               
        plane_priority = priority.lower() if priority else "none"
        if plane_priority not in ["urgent", "high", "medium", "low", "none"]:
            plane_priority = "none"
            
        payload = {
            "name": title,
            "description_html": f"<p>{description}</p>",
            "priority": plane_priority
        }
        if due_date:
            payload["target_date"] = str(due_date)
            
        if assignee_id:
            user_uuid = await self.get_user_id(assignee_id)
            if user_uuid:
                payload["assignees"] = [user_uuid]
            
        logger.info(f"PLANE PROVIDER: Creating issue in project {project}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=self.headers, timeout=10.0)
                if response.status_code >= 400:
                    logger.error(f"Plane API error response: {response.text}")
                response.raise_for_status()
                data = response.json()
                
                issue_id = data.get("id")
                issue_url = f"https://app.plane.so/{self.workspace_slug}/projects/{project}/issues/{issue_id}"
                
                return ProviderTaskResult(
                    provider_task_id=issue_id,
                    provider_task_url=issue_url
                )
                
        except Exception as e:
            logger.error(f"Plane API Error: {e}")
            raise ProviderError(f"Failed to create Plane issue: {e}")
            
    async def get_user_id(self, email_or_name: str) -> Optional[str]:
        if not self._members_cache:
            url = f"{self.base_url}/workspaces/{self.workspace_slug}/members/"
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, headers=self.headers, timeout=10.0)
                    response.raise_for_status()
                    self._members_cache = response.json()
            except Exception as e:
                logger.error(f"Failed to fetch Plane members: {e}")
                return None
                
        search_key = email_or_name.lower().strip()
        for member_data in self._members_cache:
                                                                                     
                                                          
            m = member_data
            if search_key in (m.get("email", "").lower(), m.get("display_name", "").lower(), m.get("first_name", "").lower() + " " + m.get("last_name", "").lower()):
                return m.get("id")
        return None
