import json
import os
from typing import Generator, List, Optional

import httpx


class OpenRouterError(RuntimeError):
    pass


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default

    try:
        return float(value)
    except ValueError:
        return default


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default

    try:
        return int(value)
    except ValueError:
        return default


def _build_headers() -> dict:
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    app_url = os.getenv("OPENROUTER_APP_URL", "")
    app_name = os.getenv("OPENROUTER_APP_NAME", "")

    if not api_key:
        raise OpenRouterError("OPENROUTER_API_KEY is not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    if app_url:
        headers["HTTP-Referer"] = app_url
    if app_name:
        headers["X-Title"] = app_name

    return headers


def chat(messages: List[dict], model: Optional[str] = None) -> dict:
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    default_model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct")
    system_prompt = os.getenv("OPENROUTER_SYSTEM_PROMPT", "").strip()
    temperature = _get_float("OPENROUTER_TEMPERATURE", 0.2)
    top_p = _get_float("OPENROUTER_TOP_P", 0.9)
    max_tokens = _get_int("OPENROUTER_MAX_TOKENS", 512)
    url = f"{base_url}/chat/completions"
    if system_prompt and (not messages or messages[0].get("role") != "system"):
        messages = [{"role": "system", "content": system_prompt}, *messages]

    payload = {
        "model": model or default_model,
        "messages": messages,
        "stream": False,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
    }

    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, headers=_build_headers(), json=payload)

    if response.status_code >= 400:
        raise OpenRouterError(response.text)

    return response.json()


def stream_chat(messages: List[dict], model: Optional[str] = None) -> Generator[str, None, None]:
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    default_model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct")
    system_prompt = os.getenv("OPENROUTER_SYSTEM_PROMPT", "").strip()
    temperature = _get_float("OPENROUTER_TEMPERATURE", 0.2)
    top_p = _get_float("OPENROUTER_TOP_P", 0.9)
    max_tokens = _get_int("OPENROUTER_MAX_TOKENS", 512)
    url = f"{base_url}/chat/completions"
    if system_prompt and (not messages or messages[0].get("role") != "system"):
        messages = [{"role": "system", "content": system_prompt}, *messages]

    payload = {
        "model": model or default_model,
        "messages": messages,
        "stream": True,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
    }

    with httpx.stream("POST", url, headers=_build_headers(), json=payload, timeout=60.0) as response:
        if response.status_code >= 400:
            raise OpenRouterError(response.text)

        for line in response.iter_lines():
            if not line:
                continue

            if line.startswith("data:"):
                data = line[len("data:") :].strip()
                if data == "[DONE]":
                    return

                try:
                    payload = json.loads(data)
                except json.JSONDecodeError:
                    continue

                delta = payload.get("choices", [{}])[0].get("delta", {})
                content = delta.get("content")
                if content:
                    yield content
