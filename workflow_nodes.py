"""
Module for workflow nodes.
"""
from typing import Any

from pydantic import BaseModel

from google.adk import Event
from google.adk.workflow import node


class GuardOutput(BaseModel):
    allowed: bool
    text: str

class GuardException(Exception):
    pass

@node
def fema_guard_node(node_input: dict[str, Any]) -> Event:
    print(node_input)
    if node_input:
        if node_input["allowed"]:
            return Event(output=node_input["text"])

    raise GuardException("The request contains data that violates our acceptance policy.")
