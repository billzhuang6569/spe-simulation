from plugins.llm import validate_response, DummyLLM, OpenRouterLLM
import json
from io import BytesIO
from unittest.mock import patch
import pytest


def test_validate_response_ok():
    text = '{"name": "MOVE", "arguments": {"target": [1, 2]}}'
    assert validate_response(text) == {"name": "MOVE", "arguments": {"target": [1, 2]}}


def test_validate_response_bad_json():
    assert validate_response('not json') is None


def test_validate_response_too_long():
    long_text = '{"a": "%s"}' % ('x' * 201)
    assert validate_response(long_text) is None


def test_dummy_llm_query():
    llm = DummyLLM()
    resp = llm.query('hi')
    assert resp == {"name": "MOVE", "arguments": {"target": [0, 0]}}


def test_openrouter_llm_query(monkeypatch):
    content = json.dumps({"name": "MOVE", "arguments": {"target": [0, 0]}})
    api_response = {"choices": [{"message": {"content": content}}]}

    class FakeResp(BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    fake_body = json.dumps(api_response).encode()

    def fake_urlopen(req):
        return FakeResp(fake_body)

    monkeypatch.setenv('OPENROUTER_APIKEY', 'test')
    monkeypatch.setenv('OPENROUTER_BASEURL', 'http://example.com')

    with patch('urllib.request.urlopen', fake_urlopen):
        llm = OpenRouterLLM(model='any')
        resp = llm.query('hi')
    assert resp == {"name": "MOVE", "arguments": {"target": [0, 0]}}


def test_openrouter_llm_no_key(monkeypatch):
    monkeypatch.delenv('OPENROUTER_APIKEY', raising=False)
    llm = OpenRouterLLM()
    with pytest.raises(RuntimeError):
        llm.query('hi')

