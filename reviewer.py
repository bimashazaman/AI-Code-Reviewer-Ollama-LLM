from typing import Any, Optional

import ollama

from prompts import SYSTEM_PROMPT, DIFF_SYSTEM_PROMPT, build_user_message

DEFAULT_MODEL = "qwen2.5-coder"


class ReviewError(Exception):
    """Custom exception for review-related errors."""
    pass


def _get_reply_content(response: Any) -> str:
    """Extract the assistant's reply content from an Ollama response."""
    message = getattr(response, "message", None) or response.get("message", {})
    if isinstance(message, dict):
        return message.get("content", "").strip()
    return getattr(message, "content", "").strip()


def review(
    code: str,
    model: str = DEFAULT_MODEL,
    language: Optional[str] = None,
    context: Optional[str] = None,
    is_diff: bool = False,
) -> str:
    """
    Review the provided code, codebase, or PR diff using the specified Ollama model.
    """
    if not code.strip():
        raise ReviewError("No code provided to review.")

    user_message = build_user_message(code, language=language, context=context, is_diff=is_diff)
    system_prompt = DIFF_SYSTEM_PROMPT if is_diff else SYSTEM_PROMPT

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
    except Exception as exc:
        raise ReviewError(
            f"Could not reach Ollama. Make sure it is running and run: ollama pull {model}\n"
            f"Details: {exc}"
        ) from exc

    content = _get_reply_content(response)
    if not content:
        raise ReviewError("Ollama returned an empty review.")

    return content
