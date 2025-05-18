import os
import re
from datetime import datetime
import psycopg2


LOG_TIME_FORMAT = "%a %b %d %H:%M:%S %Y"


LOG_LINE_REGEX = re.compile('^\[(?P<datetime>[A-Za-z]{3} \w{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})\]\s+\[(?P<level>\w+)\]\s+(?P<message>.+)$')


def parse_log_line(line):
    match = LOG_LINE_REGEX.match(line)
    if match:
        dt_str = match.group('datetime')
        level = match.group('level')
        message = match.group('message')
        try:
            dt = datetime.strptime(dt_str, LOG_TIME_FORMAT)
        except ValueError:
            dt = None

        return dt, level, message
    return None, None, None


def create_error_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS log_errors (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                level VARCHAR(10) NOT NULL,
                type VARCHAR(30) NOT NULL,
                message TEXT NOT NULL
            )
        """)
        conn.commit()


def insert_error(conn, dt, level, type, message):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO log_errors (timestamp, level, type, message)
            VALUES (%s, %s, %s, %s)
        """, (dt, level, type, message))
        conn.commit()


def analyze_logs(logfile_path, conn):
    errors = []
    critical_errors = []
    jk_errors = []

    with open(logfile_path, 'r', encoding='utf-8') as f:
        for line in f:
            dt, level, message = parse_log_line(line)

            if level in ('error', 'crit', 'alert', 'emerg'):
                errors.append((dt, level, message))
                insert_error(conn, dt, level, "error",  message)

            if 'mod_jk' in message:
                jk_errors.append((dt, message))
                insert_error(conn, dt, level, "mod_jk", message)

            if 'error' in message.lower() and 'child' in message:
                critical_errors.append((dt, message))
                insert_error(conn, dt, level, "critical_error", message)



if __name__ == "__main__":
    log_path = 'Apache_2k.log'

    conn = psycopg2.connect(
        dbname=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT']
    )

    create_error_table(conn)
    analyze_logs(log_path, conn)
