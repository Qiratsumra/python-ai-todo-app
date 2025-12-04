import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional


@dataclass
class Task:
    """Represents a single task in the to-do list."""

    title: str
    description: str
    completed: bool = False
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    priority: int = 0
    tags: List[str] = field(default_factory=list)
    due_date: Optional[date] = None
    recurrence_pattern: Optional[str] = None
    next_recurrence_date: Optional[date] = None
    recurrence_start_date: Optional[date] = None
    recurrence_end_date: Optional[date] = None
    reminder_time: Optional[datetime] = None
