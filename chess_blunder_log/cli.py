"""Command-line interface for the chess blunder logger."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone

from .fen import board_ascii, validate_fen
from .models import Entry
from .quiz import pick_random, quiz_display, run_quiz_entry
from .storage import Storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chess-blunder-log",
        description="Log chess blunders and lessons from played games (FEN/PGN).",
    )
    parser.add_argument(
        "--storage",
        default="entries.json",
        help="Path to the local JSON storage file (default: entries.json)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new blunder/lesson entry")
    p_add.add_argument("--game-source", required=True, help="Where the game was played")
    p_add.add_argument("--fen", required=True, help="FEN of the blunder position")
    p_add.add_argument("--move", required=True, help="The blunder move (SAN or UCI)")
    p_add.add_argument("--lesson", required=True, help="Lesson learned")
    p_add.add_argument("--pgn", default="", help="PGN snippet leading to the blunder")
    p_add.add_argument("--rating", type=int, default=None, help="Player rating at the time")
    p_add.add_argument("--tags", nargs="*", default=[], help="Tags for the entry")

    sub.add_parser("list", help="List all entries")
    p_show = sub.add_parser("show", help="Show details of one entry")
    p_show.add_argument("id", help="Entry ID")

    sub.add_parser("quiz", help="Run a review quiz over logged entries")

    p_delete = sub.add_parser("delete", help="Delete an entry")
    p_delete.add_argument("id", help="Entry ID")

    sub.add_parser("stats", help="Show summary statistics")
    return parser


def cmd_add(args: argparse.Namespace, storage: Storage) -> int:
    fen = args.fen
    if not validate_fen(fen):
        print(f"Error: invalid FEN: {fen}", file=sys.stderr)
        return 1

    move = args.move
    try:
        import chess

        board = chess.Board(fen)
        try:
            board.parse_san(move)
        except ValueError:
            try:
                board.parse_uci(move)
            except ValueError:
                print(f"Error: invalid move '{move}' for FEN {fen}", file=sys.stderr)
                return 1
    except ImportError:
        pass

    entry = Entry.new(
        game_source=args.game_source,
        position_fen=fen,
        move=move,
        lesson=args.lesson,
        pgn_snippet=args.pgn,
        rating=args.rating,
        tags=args.tags,
    )
    storage.add(entry)
    print(f"Added entry {entry.id}")
    return 0


def cmd_list(args: argparse.Namespace, storage: Storage) -> int:
    entries = storage.load()
    if not entries:
        print("No entries yet.")
        return 0
    for entry in entries:
        print(
            f"{entry.id}  {entry.created_at[:10]}  {entry.game_source}  "
            f"{entry.move}  {entry.lesson[:60]}"
        )
    return 0


def cmd_show(args: argparse.Namespace, storage: Storage) -> int:
    entry = storage.find(args.id)
    if entry is None:
        print(f"Entry not found: {args.id}", file=sys.stderr)
        return 1
    print(f"ID:        {entry.id}")
    print(f"Created:   {entry.created_at}")
    print(f"Source:    {entry.game_source}")
    print(f"Rating:    {entry.rating if entry.rating is not None else '-'}")
    print(f"Tags:      {', '.join(entry.tags) if entry.tags else '-'}")
    print(f"Move:      {entry.move}")
    print(f"Lesson:    {entry.lesson}")
    print(f"PGN:       {entry.pgn_snippet or '-'}")
    print(f"FEN:       {entry.position_fen}")
    print()
    print(
        board_ascii(entry.position_fen)
        if validate_fen(entry.position_fen)
        else f"(invalid FEN: {entry.position_fen})"
    )
    print(f"Reviews:   {entry.reviewed_count}  Last reviewed: {entry.last_reviewed or '-'}")
    return 0


def cmd_quiz(args: argparse.Namespace, storage: Storage) -> int:
    entries = storage.load()
    entry = pick_random(entries)
    if entry is None:
        print("No entries to quiz on yet. Add some with `add`.")
        return 0
    print(quiz_display(entry))
    try:
        answer = input("Your answer: ")
    except EOFError:
        print()
        return 0
    _correct, feedback = run_quiz_entry(entry, answer)
    print()
    print(feedback)
    entry.reviewed_count += 1
    entry.last_reviewed = datetime.now(timezone.utc).isoformat()
    storage.save(entries)
    return 0


def cmd_delete(args: argparse.Namespace, storage: Storage) -> int:
    if storage.delete(args.id):
        print(f"Deleted entry {args.id}")
        return 0
    print(f"Entry not found: {args.id}", file=sys.stderr)
    return 1


def cmd_stats(args: argparse.Namespace, storage: Storage) -> int:
    entries = storage.load()
    total = len(entries)
    reviewed = sum(1 for e in entries if e.reviewed_count > 0)
    print(f"Total entries: {total}")
    print(f"Reviewed at least once: {reviewed}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    storage = Storage(args.storage)
    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "show": cmd_show,
        "quiz": cmd_quiz,
        "delete": cmd_delete,
        "stats": cmd_stats,
    }
    return commands[args.command](args, storage)


if __name__ == "__main__":
    raise SystemExit(main())
