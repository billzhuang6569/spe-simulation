from lucidity.cli import main


def test_start_dummy(capsys):
    main(['start', '--dummy', '--turns', '10'])
    output = capsys.readouterr().out.strip().splitlines()
    assert len(output) == 10
    assert output[0].startswith('Turn 1')


def test_replay_dummy(tmp_path, capsys):
    log_file = tmp_path / 'session.log'
    main(['start', '--dummy', '--turns', '3', '--log', str(log_file)])
    start_output = capsys.readouterr().out.strip().splitlines()
    assert len(start_output) == 3

    main(['replay', str(log_file)])
    replay_output = capsys.readouterr().out.strip().splitlines()
    assert replay_output == start_output
