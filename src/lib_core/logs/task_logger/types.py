from dataclasses import dataclass
from enum import Enum


class TaskLoggerUpdate(Enum):
    INTERVAL = 0
    """Update only at intervals (default)"""
    UPDATE = 1
    """Update on every call to update()"""
    ALL = 2
    """Update on every call to update() and at intervals"""


@dataclass(frozen=True)
class TaskLoggerMsg:
    start: str = "Starting task..."
    end: str = "Finished task in {duration}"
    end_w_size: str = "Finished task in {duration} ({duration_per_unit}/{unit})"
    progress: str = "Still running... (elapsed: {current}s)"
    progress_w_current: str = (
        "Still running... (elapsed: {current}s, processed: {current_size}{size_unit})"
    )
    progress_w_size_and_current: str = "Still running... (elapsed: {current}s, processed: {current_size}/{size}{size_unit})"
