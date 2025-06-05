from lucidity.cli import main


def test_start_dummy(capsys):
    main(['start', '--dummy', '--turns', '10'])
    output = capsys.readouterr().out.strip().splitlines()
    assert len(output) == 10
    assert output[0].startswith('Turn 1')


def test_replay_dummy(tmp_path, capsys):
    log_file = tmp_path / 'session.db'
    main(['start', '--dummy', '--turns', '3', '--log', str(log_file)])
    start_output = capsys.readouterr().out.strip().splitlines()
    assert len(start_output) == 3

    main(['replay', str(log_file)])
    replay_output = capsys.readouterr().out.strip().splitlines()
    assert replay_output == start_output


def test_replay_websocket(tmp_path, capsys):
    log_file = tmp_path / 'session.db'
    main(['start', '--dummy', '--turns', '2', '--log', str(log_file)])
    start_output = capsys.readouterr().out.strip().splitlines()

    from starlette.testclient import TestClient
    from starlette.websockets import WebSocketDisconnect
    from lucidity.ws import create_replay_app

    app = create_replay_app(str(log_file))
    client = TestClient(app)
    with client.websocket_connect('/ws') as ws:
        received = []
        try:
            while True:
                received.append(ws.receive_text())
        except WebSocketDisconnect:
            pass

    assert received == start_output
