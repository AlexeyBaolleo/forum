import logging 
import json
from datetime import datetime, timezone
from typing import Any

from app.core.exceptions import LevelNotFoundException

_LOG_RECORD_BUILTIN_ATTRS = frozenset(
	{
		"args",
		"asctime",
		"created",
		"exc_info",
		"exc_text",
		"filename",
		"funcName",
		"levelname",
		"levelno",
		"lineno",
		"module",
		"msecs",
		"message",
		"msg",
		"name",
		"pathname",
		"process",
		"processName",
		"relativeCreated",
		"stack_info",
		"thread",
		"threadName",
	}
)

class JSONFormatter(logging.Formatter):
	"""Форматирует событие как одну строку JSON"""

	def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
		dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
		return dt.isoformat()

	def format(self, record: logging.LogRecord) -> str:
		log_data: dict[str, Any] = {
			"timestamp": self.formatTime(record),
			"process": record.process,
			"thread": record.thread,
			"level": record.levelname,
			"logger": record.name,
			"module": record.module,
			"func": record.funcName,
			"line": record.lineno,
			"message": record.getMessage(),
		}
		
		if record.exc_info:
			exc_type, exc_value, _ = record.exc_info

			tb_string = self.formatException(record.exc_info)

			log_data["exception"] = {
				"type": exc_type.__name__ if exc_type else "UnknownException",
				"message": str(exc_value),
				"traceback": tb_string,
    		}

		if record.stack_info:
			log_data["stack_info"] = record.stack_info

		for key, value in record.__dict__.items():
			if key not in _LOG_RECORD_BUILTIN_ATTRS:
				log_data[key] = value
				
		return json.dumps(
			log_data,
			ensure_ascii=False,
			default=str,
		)


def configure_logging(level: str = "DEBUG"):
	root_logger = logging.getLogger()
	
	if root_logger.handlers:
		root_logger.handlers.clear()
	
	numeric_level = logging.getLevelNamesMapping().get(level.upper())
	if not numeric_level:
		raise LevelNotFoundException()

	root_logger.setLevel(numeric_level)
	formatter = JSONFormatter()

	from sys import stdout
	stdout_logger = logging.StreamHandler(stdout)
	stdout_logger.setFormatter(formatter)
	stdout_logger.setLevel(logging.DEBUG)
	stdout_logger.addFilter(lambda record: record.levelno < logging.WARNING)

	from sys import stderr
	stderr_logger = logging.StreamHandler(stderr)
	stderr_logger.setFormatter(formatter)
	stderr_logger.setLevel(logging.WARNING)
	
	root_logger.addHandler(stdout_logger)
	root_logger.addHandler(stderr_logger)