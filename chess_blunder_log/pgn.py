"""PGN snippet parsing helpers."""

from __future__ import annotations

import io
import re

import chess
import chess.pgn


def parse_pgn_moves(snippet: str) -> list[str]:
    """Parse a PGN snippet into a list of SAN moves.

    Falls back to regex move extraction when the snippet is not a valid PGN
    stream. Returns an empty list for empty/invalid input.
    """
    if not snippet or not snippet.strip():
        return []

    game = chess.pgn.read_game(io.StringIO(snippet))
    if game is not None:
        return [node.san() for node in game.mainline() if node.san()]

    moves: list[str] = []
    board = chess.Board()
    for san in _extract_raw_moves(snippet):
        try:
            move = board.parse_san(san)
        except ValueError:
            continue
        moves.append(board.san(move))
        board.push(move)
    return moves


def position_and_move_from_pgn(snippet: str) -> tuple[str, str]:
    """Return ``(fen, move)`` for the last move in a PGN snippet.

    The FEN describes the position *before* the final move (the blunder
    position), and ``move`` is that final move in canonical SAN. Raises
    ``ValueError`` when the snippet contains no moves.
    """
    moves = parse_pgn_moves(snippet)
    if not moves:
        raise ValueError("PGN snippet contains no moves")
    board = chess.Board()
    for san in moves[:-1]:
        board.push_san(san)
    return board.fen(), board.san(board.parse_san(moves[-1]))


def _extract_raw_moves(snippet: str) -> list[str]:
    text = re.sub(r"\[[^\]]*\]", " ", snippet)
    text = re.sub(r"\d+\.\.\.?\s*", " ", text)
    text = re.sub(r"\d+\.\s*", " ", text)
    text = re.sub(r"[0-9]+\s*$", "", text)
    tokens = re.findall(
        r"O-O-O|O-O|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8][+#]?|[KQRBN][a-h][1-8][+#]?",
        text,
    )
    return tokens
