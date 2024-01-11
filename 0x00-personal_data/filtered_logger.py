#!/usr/bin/env python3
"""Filter, logger module
"""
import os
import re
import logging
import mysql.connector
from mysql.connector.connection import MySQLConnection
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates log message fields based on specified criteria.

    Args:
    fields (list): A list of strings representing all fields to obfuscate.
    redaction (str): A string representing by what the field will be obfuscated
    message (List[str}): A list of string representing the log line.
    separator (str): A string representing by which character is separating all
                     fields in the log line (message).

    Returns:
    str: The obfuscated log message.

    """
    for field in fields:
        pattern = re.escape(field) + r'=.*?' + re.escape(separator)
        replacement = field + '=' + redaction + separator
        message = re.sub(pattern, replacement, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        redact the message of LogRecord instance
        Args:
        record (logging.LogRecord): LogRecord instance containing message
        Return:
            formatted string
        """
        message = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(self.fields, self.REDACTION,
                                message, self.SEPARATOR)
        return redacted


def get_logger() -> logging.Logger:
    """Return a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()

    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> MySQLConnection:
    """Connect to secure database
    """
    username: str = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password: str = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host: str = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database: str = os.getenv("PERSONAL_DATA_DB_NAME")

    # Connect to the MySQL database
    try:
        db: MySQLConnection = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )
        return db
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        raise


def main():
    """Entry point
    """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
