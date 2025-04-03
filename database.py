import sqlite3
from datetime import datetime
import string
import random

def get_db_connection():
    conn = sqlite3.connect('instance/url_shortener.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            clicks INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def add_url(original_url):
    conn = get_db_connection()
    short_code = generate_short_code()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        conn.execute(
            'INSERT INTO urls (original_url, short_code, created_at) VALUES (?, ?, ?)',
            (original_url, short_code, created_at)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # If short_code already exists, try again
        conn.close()
        return add_url(original_url)
    
    conn.close()
    return short_code

def get_original_url(short_code):
    conn = get_db_connection()
    url = conn.execute(
        'SELECT original_url FROM urls WHERE short_code = ?',
        (short_code,)
    ).fetchone()
    conn.close()
    return url['original_url'] if url else None

def increment_clicks(short_code):
    conn = get_db_connection()
    conn.execute(
        'UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?',
        (short_code,)
    )
    conn.commit()
    conn.close()

def get_url_stats(short_code):
    conn = get_db_connection()
    stats = conn.execute(
        'SELECT original_url, short_code, created_at, clicks FROM urls WHERE short_code = ?',
        (short_code,)
    ).fetchone()
    conn.close()
    return stats