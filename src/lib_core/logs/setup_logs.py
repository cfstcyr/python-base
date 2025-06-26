import asyncio
import logging
import sys
import threading
from types import TracebackType
from typing import Any

import structlog

from lib_core.settings.env_settings import EnvSettings

from .logs_settings import LogsSettings


def _setup_exception_handlers(log: structlog.stdlib.BoundLogger) -> None:
    def handle_exception(
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            return sys.__excepthook__(exc_type, exc_value, exc_traceback)
        log.critical(
            "uncaught_exception",
            exc_info=(exc_type, exc_value, exc_traceback),  # noqa: LOG014
        )
        return None

    sys.excepthook = handle_exception

    def thread_exception_handler(args: threading.ExceptHookArgs):
        log.critical(
            "uncaught_thread_exception",
            thread=args.thread.name if args.thread else "unknown",
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),  # noqa: LOG014
        )

    threading.excepthook = thread_exception_handler

    def async_exception_handler(_: Any, context: dict[str, Any]):
        msg = context.get("message", "unhandled_asyncio_exception")
        exc = context.get("exception")
        log.critical(msg, exc_info=exc)

    asyncio.get_event_loop().set_exception_handler(async_exception_handler)


def map_level_to_severity(
    _logger: Any, _method_name: str, event_dict: structlog.typing.EventDict
) -> structlog.typing.EventDict:
    level = event_dict.pop("level", None)
    if level:
        event_dict["severity"] = level.upper()
    return event_dict


def setup_logs(logs_settings: LogsSettings, env_settings: EnvSettings):
    is_dev = env_settings.is_dev()
    level = logs_settings.dev_log_level if is_dev else logs_settings.log_level

    # Basic stdlib logging config
    logging.basicConfig(
        level=level,
        format="%(message)s",
        stream=sys.stdout,
    )

    # Select renderer
    renderer = (
        structlog.dev.ConsoleRenderer()
        if is_dev
        else structlog.processors.JSONRenderer()
    )

    # Shared processors
    pre_chain: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if not is_dev:
        pre_chain += [
            structlog.processors.format_exc_info,
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.MODULE,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                }
            ),
        ]
        if logs_settings.is_gcp:
            pre_chain.append(map_level_to_severity)

    # Setup stdlib Formatter that wraps structlog processor chain
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=pre_chain,
    )

    # Apply formatter to all stdlib handlers
    for handler in logging.getLogger().handlers:
        handler.setFormatter(formatter)

    for logger_name in logs_settings.logger_names + logs_settings.logger_names_extends:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        for handler in logger.handlers:
            handler.setFormatter(formatter)

    # Configure structlog
    structlog.configure(
        processors=[
            *pre_chain,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(level),
        cache_logger_on_first_use=True,
    )

    # Setup uncaught exception hooks
    _setup_exception_handlers(structlog.get_logger("uncaught"))
