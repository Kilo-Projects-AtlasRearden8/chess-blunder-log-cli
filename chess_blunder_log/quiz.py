"""Review quiz over logged blunder entries."""

from __future__ import annotations

import random
import re
from collections.abc import Sequence

from .fen import board_ascii, validate_fen
from .models import Entry


def pick_random(entries: Sequence[Entry]) -> Entry | None:
    """Pick a random entry, preferring ones reviewed the fewest times."""
    if not entries:
        return None
    min_reviews = min(e.reviewed_count for e in entries)
    candidates = [e for e in entries if e.reviewed_count == min_reviews]
    return random.choice(candidates)


def run_quiz_entry(entry: Entry, answer: str) -> tuple[bool, str]:
    """Check a free-text answer against an entry's lesson/move.

    Returns (correct, feedback).
    """
    normalized = answer.strip().lower()
    lesson_words = [w for w in re.split(r"\W+", entry.lesson.lower()) if w]
    move_token = entry.move.lower().strip()

    correct = False
    if (
        normalized == move_token
        or lesson_words
        and any(word in normalized for word in lesson_words[:3])
        or normalized in entry.lesson.lower()
    ):
        correct = True

    feedback = "Correct! " if correct else "Not quite. "
    feedback += f"Move: {entry.move}. Lesson: {entry.lesson}"
    if entry.pgn_snippet:
        feedback += f"\nPGN: {entry.pgn_snippet}"
    return correct, feedback


def quiz_display(entry: Entry) -> str:
    """Build the text shown to the quiz taker for an entry."""
    lines = [
        "Review this blunder position:",
        "",
        board_ascii(entry.position_fen)
        if validate_fen(entry.position_fen)
        else f"(invalid FEN: {entry.position_fen})",
        "",
        f"Source: {entry.game_source}",
    ]
    if entry.pgn_snippet:
        lines.append(f"PGN snippet: {entry.pgn_snippet}")
    lines.append("")
    lines.append("What was the blunder move, or what is the lesson?")
    return "\n".join(lines)
