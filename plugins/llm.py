import json
from typing import Optional, Any

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
