from typing import Any
from google.adk.workflow import BaseNode
from vertexai import agent_engines

from rich.markdown import Markdown
from rich.console import Console

from workflow_nodes import GuardException

_CONSOLE = Console()


async def run_remote_agent_prompt(remote_agent: Any,
                                  prompt: str,
                                  user_id: str = "user_123"):
    latest_event: dict[str, Any] = {}
    try:
        async for event in remote_agent.async_stream_query(user_id=user_id,
                                                        message=prompt):
            latest_event = event

        
            response = latest_event.get("content", {}).get("parts", [{
                "text": ""
            }])[0].get("text", "")
            _CONSOLE.print(Markdown(response))
    except GuardException as e:
        _CONSOLE.print(Markdown(str(e)))


class AgentTester:

    def __init__(self,
                 agent: BaseNode,
                 app_name: str = "App",
                 user_id: str = "user_123"):
        self._app = agent_engines.AdkApp(agent=agent, app_name=app_name)
        self.app_name = app_name
        self._user_id = user_id

    async def run_prompt(self, prompt: str):
        response = ""
        latest_event: dict[str, Any] = {}

        try:
            async for event in self._app.async_stream_query(user_id=self._user_id, message=prompt):
                latest_event = event
                response = latest_event.get("content", {}).get("parts", [{"text": ""}])[0].get("text", "")
                _CONSOLE.print(Markdown(response))
        except GuardException as e:
            _CONSOLE.print(Markdown(str(e)))
