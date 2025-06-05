from plugins.llm import validate_response, DummyLLM


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
