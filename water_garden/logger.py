import logging

logger = logging.getLogger(__name__)


shell_handler = logging.StreamHandler()
file_handler = logging.FileHandler("debug.log")

logger.setLevel(logging.INFO)
shell_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.INFO)


fmt_shell = '%(levelname)s %(asctime)s %(message)s'
fmt_file = '%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'

shell_formatter = logging.Formatter(fmt_shell)
file_formatter = logging.Formatter(fmt_file)


shell_handler.setFormatter(shell_formatter)
file_handler.setFormatter(file_formatter)

logger.addHandler(shell_handler)
logger.addHandler(file_handler)
