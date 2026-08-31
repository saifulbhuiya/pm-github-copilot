import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from db import init_db, get_user_board, move_card, create_card, delete_card, rename_column
from models import BoardData, CreateCardRequest, MoveCardRequest, RenameColumnRequest

load_dotenv()

app = FastAPI(title="Project Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    print("WARNING: OPENROUTER_API_KEY not found in environment variables")

# Initialize database on startup
init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from API"}


@app.get("/api/boards/user", response_model=BoardData)
def get_board():
    """Get user's board (MVP: hardcoded user_id=1)"""
    board = get_user_board(1)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@app.post("/api/cards")
def add_card(request: CreateCardRequest):
    """Create new card"""
    try:
        card_id = create_card(request.column_id, request.title, request.details)
        return {"id": str(card_id), "title": request.title, "details": request.details}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/cards/{card_id}")
def move_card_endpoint(card_id: int, request: MoveCardRequest):
    """Move card to different column"""
    try:
        move_card(1, card_id, request.column_id, request.position)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/cards/{card_id}")
def delete_card_endpoint(card_id: int):
    """Delete card"""
    try:
        delete_card(card_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/columns/{column_id}")
def rename_column_endpoint(column_id: int, request: RenameColumnRequest):
    """Rename column"""
    try:
        rename_column(column_id, request.title)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Serve static frontend files from Next.js export output
static_dir = Path(__file__).parent.parent / "frontend" / "out"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="frontend")
else:
    print(f"WARNING: Static files directory not found at {static_dir}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
