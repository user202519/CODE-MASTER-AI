import sqlite3
from config import DATABASE


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        user_message TEXT NOT NULL,
        bot_reply TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_chat(session_id, user_message, bot_reply):
    conn = get_connection()

    conn.execute("""
        INSERT INTO chats(
            session_id,
            user_message,
            bot_reply
        )
        VALUES(?,?,?)
    """, (session_id, user_message, bot_reply))

    conn.commit()
    conn.close()


def get_chats(session_id):
    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM chats
        WHERE session_id=?
        ORDER BY id ASC
    """, (session_id,)).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_sessions():
    conn = get_connection()

    rows = conn.execute("""
        SELECT
            session_id,
            MIN(id) AS first_id
        FROM chats
        GROUP BY session_id
        ORDER BY first_id DESC
    """).fetchall()

    sessions = []

    for row in rows:
        first = conn.execute("""
            SELECT user_message
            FROM chats
            WHERE id=?
        """, (row["first_id"],)).fetchone()

        sessions.append({
            "session_id": row["session_id"],
            "title": first["user_message"][:40] if first else "New Chat"
        })

    conn.close()

    return sessions


def delete_session(session_id):
    conn = get_connection()

    conn.execute("""
        DELETE FROM chats
        WHERE session_id=?
    """, (session_id,))

    conn.commit()
    conn.close()