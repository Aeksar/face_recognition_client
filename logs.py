import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[{asctime}] #{levelname} {filename} ({lineno}): {message}",
    style='{',
    encoding='UTF-8'
)