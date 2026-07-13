import ollama

from prompts import SYSTEM_PROMPT, build_user_message

DEFAULT_MODEL = "qwen2.5-coder"


class ReviewError(Exception):
    pass


def _get_reply_content(response):
    """Read the assistant message from an Ollama response."""
    message = getattr(response, "message", None) or response.get("message", {})
    if isinstance(message, dict):
        return message.get("content", "").strip()
    return getattr(message, "content", "").strip()


def review(code, model=DEFAULT_MODEL, language=None, context=None):
    if not code.strip():
        raise ReviewError("No code provided.")

    user_message = build_user_message(code, language=language, context=context)

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
    except Exception as exc:
        raise ReviewError(
            f"Could not reach Ollama. Make sure it is running and run: ollama pull {model}"
        ) from exc

    content = _get_reply_content(response)
    if not content:
        raise ReviewError("Ollama returned an empty review.")

    return content
