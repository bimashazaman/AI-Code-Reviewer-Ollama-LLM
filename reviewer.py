from typing import Optional

import ollama

from prompts import SYSTEM_PROMPT

DEFAULT_MODEL = "qwen2.5-coder"


class ReviewError(Exception):
    """Raised when a code review cannot be completed."""


def review(
    code: str,
    model: str = DEFAULT_MODEL,
    language: Optional[str] = None,
) -> str:
    if not code.strip():
        raise ReviewError("No code provided.")

    user_content = code.strip()
    if language:
        user_content = f"Language: {language}\n\n```\n{user_content}\n```"

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
        )
    except Exception as exc:
        raise ReviewError(
            "Failed to reach Ollama. Make sure the Ollama app is running and "
            f"the '{model}' model is installed (`ollama pull {model}`)."
        ) from exc

    return response["message"]["content"]
