"""JSON storage for blunder entries."""

from __future__ import annotations

import json
import os
from pathlib import Path

from .models import Entry


class Storage:
    """Read/write entries to a local JSON file."""

    def __init__(self, path: str | os.PathLike[str] = "entries.json") -> None:
        self.path = Path(path)

    def load(self) -> list[Entry]:
        if not self.path.exists():
            return []
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, OSError):
            return []
        if not isinstance(data, list):
            return []
        entries: list[Entry] = []
        for item in data:
            if isinstance(item, dict):
                try:
                    entries.append(Entry.from_dict(item))
                except (KeyError, TypeError):
                    continue
        return entries

    def save(self, entries: list[Entry]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [entry.to_dict() for entry in entries]
        tmp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
        os.replace(tmp_path, self.path)

    def add(self, entry: Entry) -> None:
        entries = self.load()
        entries.append(entry)
        self.save(entries)

    def delete(self, entry_id: str) -> bool:
        entries = self.load()
        filtered = [e for e in entries if e.id != entry_id]
        if len(filtered) == len(entries):
            return False
        self.save(filtered)
        return True

    def find(self, entry_id: str) -> Entry | None:
        for entry in self.load():
            if entry.id == entry_id:
                return entry
        return None
