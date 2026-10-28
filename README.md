# chess-blunder-log

A small, local-first Python CLI for logging chess blunders and lessons from
played games, using FEN positions or PGN snippets. Entries are stored in a
local JSON file, and a built-in review quiz helps you remember what you
learned.

A fan project by **Dylan Asdale / Asdale Dynamics, LLC** (Indiana, formed
October 2026). No game assets are included or distributed. This is not
affiliated with or endorsed by any chess platform, publisher, or rights
holder.

## Install

```bash
git clone <this-repo>
cd chess-blunder-log-cli
pip install -e .
```

Requires Python 3.10+ and the `python-chess` package (installed automatically).

## Usage

Add a blunder from a game you played:

```bash
chess-blunder-log add \
  --game-source "Chess.com rapid" \
  --fen "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK1R w kq - 4 4" \
  --move "Nxe5" \
  --lesson "Don't grab material without checking tactics first" \
  --pgn "1. e4 e5 2. Nf3 Nf6 3. Nxe5 d6 4. Nf3 Nxe4 5. d4" \
  --rating 1150 \
  --tags opening,tactics
```

List your entries:

```bash
chess-blunder-log list
```

Show one entry with an ASCII board rendering:

```bash
chess-blunder-log show <entry-id>
```

Run the review quiz (pick an entry, guess the blunder move or lesson):

```bash
chess-blunder-log quiz
```

Delete an entry or see stats:

```bash
chess-blunder-log delete <entry-id>
chess-blunder-log stats
```

Use `--storage` to keep your journal in a different JSON file:

```bash
chess-blunder-log --storage ~/chess-journal.json add ...
```

## Storage

All data lives in a local JSON file (`entries.json` by default, in the current
directory). Nothing is sent anywhere. No accounts, no API keys, no network.

## Tests

```bash
pip install pytest
pytest
```

## Credits

Built by Dylan Asdale, registered nurse turned AI author and founder of
**Asdale Dynamics, LLC** — beginner-friendly AI education, books and guides,
and practical local-first tools. See *The Massive AI Manual* and
dylanasdale.github.io.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.
