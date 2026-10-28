"""Tests for entry logic and storage."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import chess

from chess_blunder_log.fen import validate_fen
from chess_blunder_log.models import Entry
from chess_blunder_log.pgn import parse_pgn_snippet
from chess_blunder_log.storage import Storage


def test_entry_new_sets_id_and_timestamp():
    entry = Entry.new(
        game_source="Chess.com rapid",
        position_fen=chess.Board().fen(),
        move="e4",
        lesson="Control the center early",
        rating=1200,
        tags=["opening"],
    )
    assert entry.id
    assert entry.created_at
    assert entry.reviewed_count == 0
    assert entry.last_reviewed is None
    assert entry.tags == ["opening"]


def test_entry_to_dict_from_dict_roundtrip():
    original = Entry.new(
        game_source="Lichess blitz",
        position_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        move="Nf3",
        lesson="Develop the knight",
        pgn_snippet="1. Nf3",
        rating=1500,
        tags=["development"],
    )
    original.reviewed_count = 2
    original.last_reviewed = "2026-10-28T12:00:00+00:00"
    restored = Entry.from_dict(original.to_dict())
    assert restored.id == original.id
    assert restored.game_source == original.game_source
    assert restored.position_fen == original.position_fen
    assert restored.move == original.move
    assert restored.lesson == original.lesson
    assert restored.pgn_snippet == original.pgn_snippet
    assert restored.rating == original.rating
    assert restored.tags == original.tags
    assert restored.reviewed_count == original.reviewed_count
    assert restored.last_reviewed == original.last_reviewed


def test_entry_defaults():
    entry = Entry.new(
        game_source="OTB",
        position_fen=chess.Board().fen(),
        move="d4",
        lesson="Queen's pawn opening",
    )
    assert entry.pgn_snippet == ""
    assert entry.rating is None
    assert entry.tags == []


def test_validate_fen_accepts_start_position():
    assert validate_fen(chess.Board().fen()) is True


def test_validate_fen_rejects_garbage():
    assert validate_fen("not a fen") is False
    assert validate_fen("") is False


def test_parse_pgn_snippet_full_game():
    fen, moves = parse_pgn_snippet("1. e4 e5 2. Nf3 Nc6 3. Bb5")
    assert moves == ["e4", "e5", "Nf3", "Nc6", "Bb5"]
    board = chess.Board()
    for san in moves:
        board.push_san(san)
    assert fen == board.fen()


def test_parse_pgn_snippet_empty():
    fen, moves = parse_pgn_snippet("")
    assert fen == chess.Board().fen()
    assert moves == []


def test_storage_add_load_delete_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "entries.json"
        storage = Storage(path)
        assert storage.load() == []
        entry = Entry.new(
            game_source="Test",
            position_fen=chess.Board().fen(),
            move="e4",
            lesson="test lesson",
        )
        storage.add(entry)
        loaded = storage.load()
        assert len(loaded) == 1
        assert loaded[0].id == entry.id
        # Disk persistence check
        raw = json.loads(path.read_text(encoding="utf-8"))
        assert len(raw) == 1
        assert storage.delete(entry.id) is True
        assert storage.load() == []
        assert storage.delete("missing-id") is False


def test_storage_missing_file_returns_empty():
    with tempfile.TemporaryDirectory() as tmp:
        storage = Storage(Path(tmp) / "nonexistent.json")
        assert storage.load() == []
