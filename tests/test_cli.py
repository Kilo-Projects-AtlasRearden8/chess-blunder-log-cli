from chess_blunder_log.cli import main


def test_cli_add_invalid_fen_fails(capsys, monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "chess-blunder-log",
            "--storage",
            "/tmp/x.json",
            "add",
            "--game-source",
            "x",
            "--fen",
            "bad",
            "--move",
            "e4",
            "--lesson",
            "y",
        ],
    )
    assert main() == 1
    assert "invalid FEN" in capsys.readouterr().err
