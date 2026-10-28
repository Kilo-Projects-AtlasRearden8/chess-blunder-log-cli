"""Data model for a logged chess blunder or lesson."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Entry:
    """A single blunder/lesson entry from a played game."""

    id: str
    created_at: str
    game_source: str
    position_fen: str
    pgn_snippet: str
    move: str
    lesson: str
    rating: int | None = None
    tags: list[str] = field(default_factory=list)
    reviewed_count: int = 0
    last_reviewed: str | None = None

    @classmethod
    def new(
        cls,
        game_source: str,
        position_fen: str,
        move: str,
        lesson: str,
        pgn_snippet: str = "",
        rating: int | None = None,
        tags: list[str] | None = None,
    ) -> Entry:
        now = datetime.now(timezone.utc).isoformat()
        return cls(
            id=str(uuid.uuid4()),
            created_at=now,
            game_source=game_source,
            position_fen=position_fen,
            pgn_snippet=pgn_snippet,
            move=move,
            lesson=lesson,
            rating=rating,
            tags=tags or [],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "game_source": self.game_source,
            "position_fen": self.position_fen,
            "pgn_snippet": self.pgn_snippet,
            "move": self.move,
            "lesson": self.lesson,
            "rating": self.rating,
            "tags": self.tags,
            "reviewed_count": self.reviewed_count,
            "last_reviewed": self.last_reviewed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Entry:
        return cls(
            id=data["id"],
            created_at=data["created_at"],
            game_source=data["game_source"],
            position_fen=data["position_fen"],
            pgn_snippet=data.get("pgn_snippet", ""),
            move=data["move"],
            lesson=data["lesson"],
            rating=data.get("rating"),
            tags=data.get("tags", []),
            reviewed_count=data.get("reviewed_count", 0),
            last_reviewed=data.get("last_reviewed"),
        )
