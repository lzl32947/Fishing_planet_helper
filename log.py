import logging, logging.handlers

logger = logging.getLogger("Runtime")
logger.setLevel(level=logging.DEBUG)
fhandler = logging.handlers.RotatingFileHandler("log/log.txt")  # Handler用于将日志记录发送至合适的目的地，如文件、终端等
fhandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)

logger.addHandler(fhandler)
logger.addHandler(console)
