import json
import os
from typing import Generator, Iterable, List, Optional

import httpx

OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct")
OPENROUTER_APP_URL = os.getenv("OPENROUTER_APP_URL", "")
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "")


class OpenRouterError(RuntimeError):
    pass


def _build_headers() -> dict:
    if not OPENROUTER_API_KEY:
        raise OpenRouterError("OPENROUTER_API_KEY is not set")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    if OPENROUTER_APP_URL:
        headers["HTTP-Referer"] = OPENROUTER_APP_URL
    if OPENROUTER_APP_NAME:
        headers["X-Title"] = OPENROUTER_APP_NAME

    return headers


def chat(messages: List[dict], model: Optional[str] = None) -> dict:
    url = f"{OPENROUTER_BASE_URL}/chat/completions"
    payload = {
        "model": model or OPENROUTER_MODEL,
        "messages": messages,
        "stream": False,
    }

    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, headers=_build_headers(), json=payload)

    if response.status_code >= 400:
        raise OpenRouterError(response.text)

    return response.json()


def stream_chat(messages: List[dict], model: Optional[str] = None) -> Generator[str, None, None]:
    url = f"{OPENROUTER_BASE_URL}/chat/completions"
    payload = {
        "model": model or OPENROUTER_MODEL,
        "messages": messages,
        "stream": True,
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
