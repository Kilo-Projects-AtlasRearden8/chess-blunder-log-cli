# STATUS

chess-blunder-log — local-first CLI for logging chess blunders and lessons.
Commit: 8b96646 (Initial release of chess-blunder-log CLI), branch: master.

## What was built

A small Python CLI (`chess_blunder_log` package) for logging chess blunders
and lessons from played games, using FEN positions or PGN snippets, with
local JSON storage and a review quiz.

Modules:
- `models.py` — `Entry` dataclass (id, created_at, game_source, position_fen,
  pgn_snippet, move, lesson, rating, tags, reviewed_count, last_reviewed) with
  `to_dict`/`from_dict` serialization and an `Entry.new` factory.
- `storage.py` — `Storage`: atomic read/write of entries to a local JSON file
  (add, load, save, delete, find).
- `fen.py` — FEN validation (`chess.Board`), ASCII board rendering.
- `pgn.py` — PGN snippet parsing into FEN + SAN move list (`python-chess`).
- `quiz.py` — review quiz: picks the least-reviewed entry, displays an ASCII
  board, checks a free-text answer against the move/lesson, tracks reviews.
- `cli.py` — argparse commands: `add`, `list`, `show`, `quiz`, `delete`,
  `stats`; `--storage` option (default `entries.json`).
- `__main__.py` — supports `python -m chess_blunder_log`.
- Console script entry point: `chess-blunder-log`.

Tests (`tests/`): `test_entry.py` (entry creation, dict roundtrip, defaults,
FEN validation, PGN parsing, storage add/load/delete roundtrip),
`test_cli.py` (invalid FEN rejected with exit 1).

Also included: `LICENSE` (MIT, "Copyright (c) 2026 Asdale Dynamics, LLC"),
`README.md` (credits Asdale Dynamics, LLC), `pyproject.toml`, `.gitignore`.
Fan project, no game assets, no network, no secrets, no personal data.

## How to run

```bash
pip install -e .        # or: pip install chess-blunder-log (requires python-chess)
chess-blunder-log --help

chess-blunder-log add \
  --game-source "Chess.com rapid" \
  --fen "rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3" \
  --move Nxe5 \
  --lesson "Don't grab material without checking tactics first" \
  --pgn "1. e4 e5 2. Nf3 Nf6" \
  --rating 1150 --tags opening,tactics

chess-blunder-log list
chess-blunder-log show <id>
chess-blunder-log quiz
chess-blunder-log stats
chess-blunder-log delete <id>
```

All data stays in a local JSON file (`entries.json` by default). Nothing is
sent anywhere.

## Verification results

- `pip install -e . --break-system-packages`: OK (console script `chess-blunder-log` installed)
- `python3 -m pytest -q`: 10 passed
- `python3 -m ruff check chess_blunder_log tests`: All checks passed
- `python3 -m ruff format --check chess_blunder_log tests`: All files formatted
- Manual CLI flows verified: add, list, show (ASCII board render), quiz
  (correct-answer feedback + review counter), stats, delete, invalid-FEN
  rejection (exit 1), delete of missing id (exit 1).

Python 3.13.5; dependencies: python-chess 1.11.2 (imported as `chess`).

## Known gaps

- Quiz answer checking is keyword/free-text based, not exact; partial lesson
  words count as correct.
- Quiz picks randomly among least-reviewed entries; no spaced-repetition
  scheduling.
- No editing of existing entries (delete and re-add instead).
- Storage path defaults to `entries.json` in the current directory; use
  `--storage` for another location.
- No `.github/workflows` files (per project constraints), no CI configured.
