import datetime
import threading
import time
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, field
from enum import Enum
from types import TracebackType
from typing import Self, TypeVar

import structlog

T = TypeVar("T")


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


@dataclass
class TaskLogger:
    """
    Logs task progress using structlog. Supports automatic and manual updates,
    duration tracking, progress display, and error logging.

    Parameters:
        logger (structlog.BoundLogger): The structlog logger to output messages to.
        name (str): Name/description of the task.
        size (int | None): Optional total number of items to process. Enables per-item timing and progress ratios.
        size_unit (str | tuple[str, str]): Unit for progress messages. Can be a single string (e.g. "items") or
                                           a tuple for singular/plural (e.g. ("item", "items")).
        progress_interval (float): Time in seconds between periodic progress logs (default: 10).
        progress_min_interval (float): Minimum interval in seconds between logs (prevents log spam, default: 3).
        progress_update (TaskLoggerUpdate): When to emit progress logs — on interval, on update call, or both.
        msg (TaskLoggerMsg): Customizable message templates for task start, progress, and end.
        auto_start (bool): If True, the task starts immediately on instantiation.
        on_error (Callable[[BaseException], None] | None): Optional callback invoked if an exception is raised.
    """

    # --- Core logger config ---
    logger: structlog.BoundLogger
    name: str

    # --- Progress config ---
    size: int | None = None
    size_unit: str | tuple[str, str] = (" item", " items")
    progress_interval: float = 10
    progress_min_interval: float = 3
    progress_update: TaskLoggerUpdate = TaskLoggerUpdate.INTERVAL

    # --- Custom messaging ---
    msg: TaskLoggerMsg = field(default_factory=TaskLoggerMsg)

    # --- Control flags ---
    auto_start: bool = False
    on_error: Callable[[BaseException], None] | None = None

    # --- Internal state (not user-facing) ---
    _start: datetime.datetime = field(init=False)
    _current: int | None = field(default=None, init=False)
    _running: bool = field(default=False, init=False)
    _progress_thread: threading.Thread | None = field(default=None, init=False)
    _last_progress_time: float = field(default_factory=time.monotonic, init=False)
    _progress_lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def __post_init__(self):
        if self.size is not None and self.size < 0:
            raise ValueError("Size must be a non-negative integer or None.")
        if self.progress_interval <= 0:
            raise ValueError("Progress interval must be a positive number.")

        if self.auto_start:
            self.start()

        self.logger = self.logger.bind(task_name=self.name)

    def start(self) -> Self:
        self._running = True
        self._start = datetime.datetime.now(tz=datetime.UTC)
        self.logger.info(self.msg.start, task_status="started")

        if self.progress_update in (TaskLoggerUpdate.INTERVAL, TaskLoggerUpdate.ALL):
            self._progress_thread = threading.Thread(
                target=self._progress_interval, daemon=True
            )
            self._progress_thread.start()

        return self

    def end(self):
        if not self._running:
            raise RuntimeError("TaskLogger has not been started or has already ended.")
        self._running = False
        duration = datetime.datetime.now(tz=datetime.UTC) - self._start

        log = self.logger.bind(
            duration=f"{duration.total_seconds():.0f}s",
            task_status="stopped",
        )

        if self.size and self.size > 0:
            log.info(
                self.msg.end_w_size.format(
                    duration=duration,
                    duration_per_unit=duration / self.size,
                    unit=self._plural_unit(self.size),
                )
            )
        else:
            log.info(self.msg.end.format(duration=duration))

    def update(self, current: int):
        if not self._running:
            raise RuntimeError("TaskLogger has not been started or has already ended.")
        with self._progress_lock:
            self._current = current

        if self.progress_update in (TaskLoggerUpdate.UPDATE, TaskLoggerUpdate.ALL):
            self._log_progress()

    def iterate(self, iterable: Iterable[T]) -> Iterator[T]:
        self._current = 0
        for i, item in enumerate(iterable, 1):
            yield item
            self.update(i)

    def _progress_interval(self):
        while self._running:
            time.sleep(self.progress_interval)
            self._log_progress()

    def _log_progress(self):
        now = time.monotonic()
        with self._progress_lock:
            if (now - self._last_progress_time) < self.progress_min_interval:
                return
            self._last_progress_time = now
            duration = datetime.datetime.now(tz=datetime.UTC) - self._start

            log = self.logger.bind(
                task_elapsed=f"{duration.total_seconds():.0f}s",
                task_status="running",
            )

            if self._current is not None:
                log = log.bind(
                    task_current=self._current,
                )
                if self.size is not None and self.size > 0:
                    log.info(
                        self.msg.progress_w_size_and_current.format(
                            current=round(duration.total_seconds()),
                            current_size=self._current,
                            size=self.size,
                            size_unit=self._plural_unit(self.size),
                        ),
                        task_total=self.size,
                        task_progress=f"{self._current / self.size:.0%}",
                    )
                else:
                    log.info(
                        self.msg.progress_w_current.format(
                            current=round(duration.total_seconds()),
                            current_size=self._current,
                            size_unit=self._plural_unit(self._current),
                        )
                    )
            else:
                log.info(
                    self.msg.progress.format(current=round(duration.total_seconds()))
                )

    def _plural_unit(self, current: int) -> str:
        if isinstance(self.size_unit, tuple):
            return self.size_unit[1 if current > 1 else 0]
        return self.size_unit

    def __enter__(self) -> Self:
        return self.start()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        if exc_val is not None:
            self.logger.error(
                "Task failed with error",
                task_name=self.name,
                error=str(exc_val),
                exc_info=(exc_type, exc_val, exc_tb),  # noqa: LOG014
            )
            if self.on_error:
                self.on_error(exc_val)
        self.end()
        return False  # propagate exception

    def __repr__(self):
        return f"<TaskLogger name={self.name!r} running={self._running}>"
