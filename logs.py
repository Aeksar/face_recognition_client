import logging

logging.basicConfig(
    level=logging.INFO,
    format="[{asctime}] #{levelname} {filename} ({lineno}): {message}",
    style='{',
    encoding='UTF-8'
)