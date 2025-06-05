import json
import os
from typing import Optional
from urllib import request

MAX_CHARS = 200


def validate_response(text: str) -> Optional[dict]:
    """Return parsed JSON if valid and under the char limit."""
    if len(text) > MAX_CHARS:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


class DummyLLM:
    """Simple LLM stub used for tests and development."""

    def __init__(self, response: Optional[dict] = None):
        self.response = response or {"name": "MOVE", "arguments": {"target": [0, 0]}}

    def query(self, prompt: str) -> Optional[dict]:
        """Return a canned response, validating JSON length."""
        text = json.dumps(self.response)
        return validate_response(text)


class OpenRouterLLM:
    """LLM client that queries the OpenRouter API."""

    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model
        self.api_key = os.getenv("OPENROUTER_APIKEY")
        self.base_url = os.getenv("OPENROUTER_BASEURL", "https://openrouter.ai/api/v1")

    def query(self, prompt: str) -> Optional[dict]:
        if not self.api_key:
            raise RuntimeError("OPENROUTER_APIKEY not set")

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        req = request.Request(
            self.base_url.rstrip("/") + "/chat/completions",
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )
        try:
            with request.urlopen(req) as resp:
                body = resp.read().decode()
            data = json.loads(body)
            content = data["choices"][0]["message"]["content"]
            return validate_response(content)
        except Exception:
            return None
