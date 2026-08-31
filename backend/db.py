import sqlite3
import json
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).parent / "kanban.db"

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db_context():
    conn = get_db()
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize database with schema and sample data"""
    if DB_PATH.exists():
        return
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Boards table
    cursor.execute("""
        CREATE TABLE boards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL DEFAULT 'My Board',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    
    # Columns table
    cursor.execute("""
        CREATE TABLE columns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            board_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            position INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(board_id) REFERENCES boards(id)
        )
    """)
    
    # Cards table
    cursor.execute("""
        CREATE TABLE cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            column_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            details TEXT DEFAULT '',
            position INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(column_id) REFERENCES columns(id)
        )
    """)
    
    # Seed demo data
    cursor.execute("INSERT INTO users (username) VALUES (?)", ("user",))
    user_id = cursor.lastrowid
    
    cursor.execute("INSERT INTO boards (user_id, title) VALUES (?, ?)", 
                   (user_id, "My Board"))
    board_id = cursor.lastrowid
    
    columns_data = [
        ("Backlog", 0),
        ("Discovery", 1),
        ("In Progress", 2),
        ("Review", 3),
        ("Done", 4),
    ]
    
    column_ids = {}
    for title, pos in columns_data:
        cursor.execute("INSERT INTO columns (board_id, title, position) VALUES (?, ?, ?)",
                      (board_id, title, pos))
        column_ids[title] = cursor.lastrowid
    
    cards_data = [
        ("Backlog", "Align roadmap themes", "Draft quarterly themes with impact statements and metrics."),
        ("Backlog", "Gather customer signals", "Review support tags, sales notes, and churn feedback."),
        ("Discovery", "Prototype analytics view", "Sketch initial dashboard layout and key drill-downs."),
        ("In Progress", "Refine status language", "Standardize column labels and tone across the board."),
        ("In Progress", "Design card layout", "Add hierarchy and spacing for scanning dense lists."),
        ("Review", "QA micro-interactions", "Verify hover, focus, and loading states."),
        ("Done", "Ship marketing page", "Final copy approved and asset pack delivered."),
        ("Done", "Close onboarding sprint", "Document release notes and share internally."),
    ]
    
    pos_per_column = {}
    for col_title, card_title, details in cards_data:
        col_id = column_ids[col_title]
        pos = pos_per_column.get(col_id, 0)
        cursor.execute(
            "INSERT INTO cards (column_id, title, details, position) VALUES (?, ?, ?, ?)",
            (col_id, card_title, details, pos)
        )
        pos_per_column[col_id] = pos + 1
    
    conn.commit()
    conn.close()

def get_user_board(user_id: int):
    """Get user's board with all columns and cards"""
    with get_db_context() as conn:
        cursor = conn.cursor()
        
        # Get board
        cursor.execute("SELECT * FROM boards WHERE user_id = ?", (user_id,))
        board_row = cursor.fetchone()
        if not board_row:
            return None
        
        board_id = board_row["id"]
        
        # Get columns
        cursor.execute(
            "SELECT id, title FROM columns WHERE board_id = ? ORDER BY position",
            (board_id,)
        )
        columns = [dict(row) for row in cursor.fetchall()]
        
        # Get cards
        cursor.execute(
            "SELECT id, column_id, title, details FROM cards WHERE column_id IN (SELECT id FROM columns WHERE board_id = ?) ORDER BY column_id, position",
            (board_id,)
        )
        cards_rows = cursor.fetchall()
        
        cards = {}
        card_ids_by_column = {col["id"]: [] for col in columns}
        
        for card_row in cards_rows:
            card_id = card_row["id"]
            col_id = card_row["column_id"]
            cards[str(card_id)] = {
                "id": str(card_id),
                "title": card_row["title"],
                "details": card_row["details"],
            }
            card_ids_by_column[col_id].append(str(card_id))
        
        # Build response format matching frontend
        return {
            "columns": [
                {
                    "id": f"col-{col['id']}",
                    "title": col["title"],
                    "cardIds": card_ids_by_column.get(col["id"], []),
                }
                for col in columns
            ],
            "cards": cards,
        }

def move_card(user_id: int, card_id: int, column_id: int, position: int):
    """Move card to different column and position"""
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE cards SET column_id = ?, position = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                      (column_id, position, card_id))
        conn.commit()
        return True

def create_card(column_id: int, title: str, details: str = ""):
    """Create new card"""
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cards (column_id, title, details, position) VALUES (?, ?, ?, (SELECT COUNT(*) FROM cards WHERE column_id = ?))",
            (column_id, title, details, column_id)
        )
        conn.commit()
        return cursor.lastrowid

def delete_card(card_id: int):
    """Delete card"""
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
        conn.commit()
        return True

def rename_column(column_id: int, title: str):
    """Rename column"""
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE columns SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                      (title, column_id))
        conn.commit()
        return True
