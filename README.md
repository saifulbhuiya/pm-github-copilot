Project Management MVP with AI Kanban Board

A full-stack Project Management application built with Next.js frontend, FastAPI backend, SQLite database, and AI-powered Kanban board management.

Features

- User authentication (hardcoded demo credentials: user/password)
- Kanban board with 5 fixed columns (Backlog, Discovery, In Progress, Review, Done)
- Drag-and-drop card management
- AI-powered assistant for card creation, movement, and deletion via natural language
- Real-time chat sidebar for AI interactions
- SQLite database with normalized schema

Tech Stack

Frontend: Next.js 16, TypeScript, Tailwind CSS 4, dnd-kit for drag-and-drop
Backend: FastAPI, Python 3.11, SQLite
AI: OpenRouter with GPT-4o-mini model
Deployment: Docker containerization
Package Manager: uv (Python), npm (Node)

Quick Start

Prerequisites

Docker and Docker Compose
.env file with OPENROUTER_API_KEY at project root

Build & Run

docker build -t pm-app:latest .
docker run -p 8000:8000 --env-file .env pm-app:latest

Access the app at http://localhost:8000

Login with:
Username: user
Password: password

Project Structure

frontend/ - Next.js application
  src/
    app/ - Page routing
    components/ - React components (KanbanBoard, LoginForm, AIChatSidebar, etc.)
    lib/ - Utilities (auth, API client, kanban logic)
backend/ - FastAPI application
  main.py - API endpoints and app initialization
  db.py - Database layer (SQLite operations)
  ai.py - OpenRouter integration
  models.py - Pydantic models for request/response
  requirements.txt - Python dependencies

Database Schema

users - User profiles
boards - Kanban boards (one per user in MVP)
columns - Board columns (fixed 5 columns)
cards - Task cards within columns

API Endpoints

Board Operations
GET /api/boards/user - Fetch user's board with columns and cards
POST /api/cards - Create new card
PUT /api/cards/{card_id} - Move card to different column
DELETE /api/cards/{card_id} - Delete card
PUT /api/columns/{column_id} - Rename column

AI Operations
POST /api/ai/chat - Send message to AI assistant for board modifications

Authentication

Frontend: LocalStorage-based session with hardcoded demo credentials
No backend authentication in MVP (single user hardcoded to user_id=1)
Session persists across page reloads

AI Integration

Sends board context to OpenRouter API
Returns structured JSON responses with action types (create, move, delete, rename)
Frontend interprets AI responses and updates board optimistically
Supports multi-card operations in single request

Testing

Frontend Tests
npm test in frontend/ directory
Covers: auth utilities, component rendering, kanban logic

Backend Tests
pytest in backend/ directory
Covers: health endpoint, CORS headers, API response format

Development Notes

The frontend uses Next.js export mode (static build) for Docker compatibility
API client implements optimistic UI updates for better UX
Database initializes with sample data on first run
AI responses include board state context for better suggestions

Future Enhancements

Multi-user support with proper authentication
Multiple boards per user
Real-time collaboration with WebSockets
Card detail editing and history tracking
Advanced filtering and search
Card attachments and comments
Sprint planning and burndown charts
