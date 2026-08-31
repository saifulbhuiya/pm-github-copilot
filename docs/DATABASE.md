# Database Architecture

## Overview

SQLite local database for Project Management MVP. Single-user focused but extensible for future multi-user/multi-board functionality.

## Schema

### Users Table
```
id (INTEGER, PK, AUTOINCREMENT)
username (TEXT, UNIQUE, NOT NULL)
created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
```

### Boards Table
```
id (INTEGER, PK, AUTOINCREMENT)
user_id (INTEGER, FK -> users.id, NOT NULL)
title (TEXT, NOT NULL, DEFAULT 'My Board')
created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
updated_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
```

### Columns Table (Kanban Columns)
```
id (INTEGER, PK, AUTOINCREMENT)
board_id (INTEGER, FK -> boards.id, NOT NULL)
title (TEXT, NOT NULL)
position (INTEGER, NOT NULL)  - Display order (0-4 for MVP)
created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
updated_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
```

### Cards Table
```
id (INTEGER, PK, AUTOINCREMENT)
column_id (INTEGER, FK -> columns.id, NOT NULL)
title (TEXT, NOT NULL)
details (TEXT, DEFAULT '')
position (INTEGER, NOT NULL)  - Display order within column
created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
updated_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
```

## Relationships

- One User has many Boards (one-to-many)
- One Board has many Columns (one-to-many, 5 fixed for MVP)
- One Column has many Cards (one-to-many)

## Initial Data

For MVP, seed with:
- One user: username="user"
- One board: title="My Board"
- Five columns: Backlog, Discovery, In Progress, Review, Done
- Eight sample cards distributed across columns

## Database File

Located at: `kanban.db` in backend root directory
Auto-created on first run if doesn't exist

## Migration Strategy

For MVP: Create tables on first startup if they don't exist (idempotent)

```python
# In backend/db.py
def init_db():
    if not db_exists():
        create_tables()
        seed_demo_data()
```

## Future Extensions

- Add indexes on frequently queried columns (user_id, board_id, column_id)
- Add updated_at indexing for pagination
- Add audit logging (who changed what, when)
- Support multiple boards per user
- Support team collaboration with permissions
- Archive/soft delete support
