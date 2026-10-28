"""PGN snippet parsing helpers."""

from __future__ import annotations

import io
import re

import chess
import chess.pgn


def parse_pgn_snippet(snippet: str) -> tuple[str, list[str]]:
    """Parse a PGN snippet into a FEN and a list of SAN moves.

    Returns (fen, moves). If the snippet cannot be parsed, returns
    the starting position FEN and an empty move list.
    """
    if not snippet or not snippet.strip():
        return chess.Board().fen(), []

    game = chess.pgn.read_game(io.StringIO(snippet))
    if game is None:
        # Try to extract raw move text between 1. and the end.
        moves = _extract_raw_moves(snippet)
        board = chess.Board()
        san_moves: list[str] = []
        for san in moves:
            try:
                move = board.parse_san(san)
                san_moves.append(board.san(move))
                board.push(move)
            except ValueError:
                break
        return board.fen(), san_moves

    board = game.end().board()
    san_moves = [node.san() for node in game.mainline() if node.san()]
    return board.fen(), san_moves


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
