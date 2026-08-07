from google.adk.agents import BaseAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from rich.markdown import Markdown
from rich.console import Console

_SESSION_SERVICE = InMemorySessionService()

_CONSOLE = Console()


class AgentTester:

    def __init__(self,
                 agent: BaseAgent,
                 app_name: str = "App",
                 user_id: str = "user_123"):
        self.app_name = app_name
        self._user_id = user_id
        self._runner = Runner(
            agent=agent,
            app_name=app_name,
            session_service=_SESSION_SERVICE,
        )

    async def run_prompt(self, prompt: str):
        session = await _SESSION_SERVICE.create_session(
            app_name=self.app_name,
            user_id=self._user_id,
        )

        content = types.Content(role="user", parts=[types.Part(text=prompt)])

        async for event in self._runner.run_async(user_id=self._user_id,
                                                  session_id=session.id,
                                                  new_message=content):
            if event.is_final_response():
                if event.content and event.content.parts:
                    _CONSOLE.print(Markdown(str(event.content.parts[0].text)))
