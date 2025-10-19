import logging
import colorlog
from core.config import LoggerConfig

# Crear logger
logger = logging.getLogger(LoggerConfig.LOG_NAME)
logger.setLevel(LoggerConfig.LOG_LEVEL)

# Formato con fecha en día/mes/año
stream_formatter = colorlog.ColoredFormatter(
    "%(asctime)s - %(log_color)s%(levelname)s%(reset)s: %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    log_colors=LoggerConfig.LOG_COLORS,
)

# Handler para stdout / stderr
stream_handler = logging.StreamHandler()
stream_handler.setLevel(LoggerConfig.LOG_LEVEL)
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)

library_loggers = (
    name
    for name in logging.root.manager.loggerDict.keys()
    if isinstance(name, str)
    and any(prefix in name for prefix in LoggerConfig.LIBRARY_LOGS_PREFIXES)
)

# Reemplazar loggers de uvicorn y fastapi por el custom
for name in library_loggers:
    # reemplazar handlers y nivel
    lib_logger = logging.getLogger(name)
    lib_logger.handlers = logger.handlers
    lib_logger.setLevel(logger.level)
    lib_logger.propagate = False  # Evitar mensajes duplicados
