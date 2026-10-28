"""FEN validation and board rendering helpers."""

from __future__ import annotations

import chess


def validate_fen(fen: str) -> bool:
    """Return True if *fen* is a valid FEN string."""
    try:
        chess.Board(fen)
    except ValueError:
        return False
    return True


def board_ascii(fen: str) -> str:
    """Return an ASCII rendering of the position described by *fen*."""
    board = chess.Board(fen)
    lines: list[str] = []
    lines.append("    a   b   c   d   e   f   g   h")
    lines.append("  +---+---+---+---+---+---+---+---+")
    for rank in range(8, 0, -1):
        row = [f"{rank} |"]
        for file in range(8):
            square = chess.square(file, rank - 1)
            piece = board.piece_at(square)
            row.append(f" {piece.symbol() if piece else '.'} |")
        lines.append("".join(row))
        lines.append("  +---+---+---+---+---+---+---+---+")
    side = "White" if board.turn else "Black"
    lines.append(f"    Side to move: {side}")
    return "\n".join(lines)


def san_from_fen_and_move(fen: str, uci: str) -> str:
    """Return the SAN for a UCI move in the position described by *fen*."""
    board = chess.Board(fen)
    move = chess.Move.from_uci(uci)
    return board.san(move)
