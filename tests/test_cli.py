from lucidity.cli import main


def test_start_dummy(capsys):
    main(['start', '--dummy', '--turns', '10'])
    output = capsys.readouterr().out.strip().splitlines()
    assert len(output) == 10
    assert output[0].startswith('Turn 1')
