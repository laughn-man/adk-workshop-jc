from typing import Optional
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai.types import Content, Part

def logging_before_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:

    if llm_request.contents:
        last = llm_request.contents[-1]
        if last.role == "user" and last.parts and last.parts[0].text:
            print(f"logging_before_callback- Agent: {callback_context.agent_name}, User entered: {last.parts[0].text.strip()}")

    return None

def bad_words_before_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:

    invalid_words = ["bomb", "trust me bro", "break"]

    if llm_request.contents:
        last = llm_request.contents[-1]
        if last.role == "user" and last.parts and last.parts[0].text:
            text = last.parts[0].text.strip().lower()

            if any(word in text for word in invalid_words):
                return LlmResponse(content=Content(role="Model", parts=[Part(text="Message violates our content guidelines.")]))

    return None


def bad_country_before_callback(
        callback_context: CallbackContext,
        llm_request: LlmRequest) -> Optional[LlmResponse]:

    invalid_countries = ["canada", "england", "india", "mexico"]

    if llm_request.contents:
        last = llm_request.contents[-1]
        if last.role == "user" and last.parts and last.parts[0].text:
            text = last.parts[0].text.strip().lower()

            if any(word in text for word in invalid_countries):
                return LlmResponse(content=Content(
                    role="Model",
                    parts=[Part(text="Location must be in the US.")]))

    return None

def log_agent_name_before_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:

    print(f"Calling agent {callback_context.agent_name}")

    return None


def chain_before_callback(callback_context: CallbackContext,
                          llm_request: LlmRequest) -> Optional[LlmResponse]:

    result = logging_before_callback(callback_context, llm_request)
    if result:
        return result

    result = bad_words_before_callback(callback_context, llm_request)
    if result:
        return result

    result = bad_country_before_callback(callback_context, llm_request)
    if result:
        return result

def logging_after_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:

    if llm_response.content and llm_response.content.parts:
        txt = llm_response.content.parts[0].text
        if txt:
            print(f"logging_after_callback- Model response: {txt}")

    return None
