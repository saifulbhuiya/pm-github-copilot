# Project Management MVP - Detailed Execution Plan

## Part 1: Planning & Documentation

**Objective:** Establish comprehensive plan with detailed sub-steps, tests, and success criteria. Get user approval before proceeding.

### Sub-steps (Checklist)

- [ ] Document existing frontend codebase in `frontend/AGENTS.md`
  - Component architecture and responsibility breakdown
  - Data structures and state management
  - Build/test scripts and development workflow
  - Integration points for future backend connection
- [ ] Enrich `docs/PLAN.md` with detailed sub-steps for all 10 parts
  - Include checklists for each part
  - Define test strategy (unit, integration, e2e)
  - Specify success criteria for each part
- [ ] Ensure user reviews and approves the enriched plan before proceeding

### Tests

- Verification checklist: All questions answered about design decisions
- Approval confirmation from user

### Success Criteria

✅ `frontend/AGENTS.md` is created and comprehensively documents existing code
✅ `docs/PLAN.md` contains detailed breakdown of all 10 parts with sub-steps, tests, and success criteria
✅ User has reviewed and approved the plan

---

## Part 2: Docker & Backend Scaffolding

**Objective:** Set up Docker infrastructure, create FastAPI backend skeleton, and write start/stop scripts. Verify with "hello world" example and test API connectivity.

### Sub-steps (Checklist)

- [ ] Create `Dockerfile` with Python 3.11+ base image
  - Install `uv` as package manager
  - Copy `backend/` into container
  - Expose port 8000 for FastAPI
  - Set up entrypoint to run FastAPI server
- [ ] Create `backend/requirements.txt` with dependencies
  - fastapi
  - uvicorn
  - python-dotenv (for .env loading)
  - Other essential packages (python-multipart, etc.)
- [ ] Create `backend/main.py` with FastAPI skeleton
  - Initialize FastAPI app
  - Load OPENROUTER_API_KEY from .env
  - Create `/health` endpoint (returns `{"status": "ok"}`)
  - Create `/api/hello` endpoint (returns `{"message": "Hello from API"}`)
  - Serve static files from `frontend/out` at root `/` path
- [ ] Create `docker-compose.yml` (optional, for future ease)
- [ ] Create platform-specific start scripts in `scripts/`
  - `scripts/start-mac.sh` - Build and run Docker container on macOS
  - `scripts/start-windows.bat` - Build and run Docker container on Windows (PowerShell or cmd)
  - `scripts/start-linux.sh` - Build and run Docker container on Linux
  - `scripts/stop-mac.sh`, `scripts/stop-windows.bat`, `scripts/stop-linux.sh` - Stop and remove container
- [ ] Test locally with Docker
  - Run start script
  - Verify Docker container is running
  - Test `/health` endpoint with curl/Invoke-WebRequest
  - Test `/api/hello` endpoint
  - Test that static files serve (will show 404 until Part 3)

### Tests

**Unit Tests (Backend):**
- Test `/health` endpoint returns correct response
- Test `/api/hello` endpoint returns correct response
- Test .env loading (OPENROUTER_API_KEY is present)

**Integration Tests:**
- Docker build succeeds without errors
- Container starts and is accessible on port 8000
- All endpoints are accessible from host machine
- Stop script cleanly shuts down container

**Manual Tests:**
- Run `scripts/start-*.sh` for your platform
- Verify container logs show server is running
- curl/PowerShell commands reach endpoints successfully
- Stop script properly terminates container

### Success Criteria

✅ Docker image builds successfully with no errors
✅ FastAPI backend runs in container on port 8000
✅ `/health` endpoint responds with `{"status": "ok"}`
✅ `/api/hello` endpoint responds with `{"message": "Hello from API"}`
✅ Start/stop scripts work correctly for the target platform
✅ OPENROUTER_API_KEY is loaded from .env without errors
✅ Container can be started and stopped cleanly

---

## Part 3: Integrate Frontend

**Objective:** Build Next.js frontend to static files and serve them from FastAPI. Verify the demo Kanban board displays at `/`. Include comprehensive unit and integration tests.

### Sub-steps (Checklist)

- [ ] Update `backend/main.py`
  - Add import for StaticFiles from fastapi.staticfiles
  - Configure to serve static files from `frontend/out` at root path `/`
  - Ensure API routes are defined before static file mounting
- [ ] Update `Dockerfile`
  - Add build stage: install Node, build frontend with `npm run build` (exports to `frontend/out`)
  - Copy built frontend files into container
  - Ensure FastAPI serves these files
- [ ] Update start/stop scripts
  - Build frontend before building Docker image (or do it in multi-stage Docker build)
  - Verify container now serves Kanban at `/`
- [ ] Test locally
  - Run start script
  - Navigate to `http://localhost:8000` in browser
  - Verify Kanban board with 5 columns and 8 cards appears
  - Test drag-and-drop functionality works
  - Test column rename works
  - Test add/delete card works

### Tests

**Unit Tests (Frontend):**
- All existing frontend tests continue to pass (KanbanBoard, KanbanColumn, KanbanCard components)
- All kanban.ts utilities pass tests (moveCard, createId, etc.)

**Integration Tests (Frontend + Backend):**
- Frontend builds successfully to static files
- FastAPI serves HTML, CSS, JS files with correct MIME types
- Frontend JS loads and hydrates correctly
- Kanban functionality works end-to-end in browser

**E2E Tests (Playwright):**
- Navigate to `http://localhost:8000`
- Verify 5 columns are visible (Backlog, Discovery, In Progress, Review, Done)
- Verify 8 cards are rendered across columns
- Drag a card between columns and verify DOM updates
- Rename a column and verify title updates
- Add a new card and verify it appears
- Delete a card and verify it's removed

### Success Criteria

✅ Frontend builds to static files in `frontend/out`
✅ Docker image includes built frontend
✅ Kanban board renders at `http://localhost:8000`
✅ All drag-drop, rename, add, delete operations work in browser
✅ Refresh page maintains in-memory state (expected for this part)
✅ All existing unit tests pass
✅ E2E tests verify full Kanban functionality

---

## Part 4: Add Authentication (Login/Logout)

**Objective:** Add login screen with hardcoded credentials ("user"/"password"). Redirect unauthenticated users to login. Add logout button. Comprehensive tests for auth flow.

### Sub-steps (Checklist)

- [ ] Create `frontend/src/components/LoginForm.tsx`
  - Form with username and password inputs
  - Submit button
  - Error message display on failed login
  - Clear form after submission
  - Use local component state (no backend call yet, just client-side validation)
- [ ] Create `frontend/src/lib/auth.ts`
  - `validateCredentials(username, password): boolean` function
    - Accept only username="user" and password="password"
  - Store auth state in localStorage (key: "user-session", value: JSON with username and token)
- [ ] Update `frontend/src/app/layout.tsx`
  - Add "use client" directive
  - Create AuthProvider context or use localStorage check
  - If not authenticated, show LoginForm instead of page children
- [ ] Update `frontend/src/app/page.tsx`
  - Assume user is authenticated (layout handles redirect)
  - Render Kanban normally
- [ ] Add logout button to Kanban header
  - Clear localStorage session
  - Redirect to login page
- [ ] Create auth-related tests

### Tests

**Unit Tests:**
- `validateCredentials()` function
  - Returns true for ("user", "password")
  - Returns false for any other combination
  - Returns false for empty credentials

**Integration Tests:**
- LoginForm component
  - Displays username/password inputs and submit button
  - Shows error on invalid credentials
  - Calls onSubmit callback on valid submit
  - Clears inputs after submit
- Auth flow end-to-end
  - Unauthenticated user sees login form
  - Submitting valid credentials sets localStorage
  - Page redirects/renders Kanban
  - Logout button clears session and returns to login

**E2E Tests (Playwright):**
- Load `http://localhost:8000`
- Verify login form appears (username/password fields, submit button)
- Try invalid login (e.g., "admin"/"admin") → error shown
- Login with "user"/"password" → redirected to Kanban board
- Verify Kanban board is displayed with 5 columns
- Click logout button → redirected back to login
- Verify session is cleared and login form appears again
- Login again → Kanban appears

### Success Criteria

✅ Unauthenticated users are shown login form before Kanban
✅ Login with "user"/"password" grants access to Kanban
✅ Invalid credentials show error message
✅ Logout clears session and returns to login
✅ Session persists across page refresh (stored in localStorage)
✅ Refresh after logout shows login form
✅ All auth unit, integration, and e2e tests pass

---

## Part 5: Database Schema & Modeling

**Objective:** Propose a SQLite database schema for the Kanban app, supporting single user per MVP. Document approach in `docs/DATABASE.md` and save schema as JSON files. Get user sign-off.

### Sub-steps (Checklist)

- [ ] Design SQLite schema for:
  - Users table (id, username, password_hash, created_at)
  - Boards table (id, user_id, title, created_at, updated_at)
  - Columns table (id, board_id, title, position, created_at, updated_at)
  - Cards table (id, column_id, title, details, position, created_at, updated_at)
- [ ] Create `docs/DATABASE.md` documenting:
  - Schema rationale (normalized design, future multi-user/multi-board ready)
  - Table relationships and foreign keys
  - Sample queries for common operations
  - Migration strategy (creating DB/tables on first run)
- [ ] Create `backend/schema.json`
  - JSON representation of table structure for documentation
  - Include column names, types, constraints
- [ ] Create `backend/sample-data.json`
  - Example data for one user with one board and sample cards
  - Shows expected structure for API responses
- [ ] Update `backend/requirements.txt`
  - Add sqlite3 (built-in with Python)
  - Add sqlalchemy (optional, for ORM) or use raw SQL
- [ ] Present plan to user for review and sign-off

### Tests

- Schema validation: All foreign keys are present and correct
- Example data confirms to schema
- Documentation is clear and comprehensive

### Success Criteria

✅ `docs/DATABASE.md` is written and comprehensive
✅ `backend/schema.json` defines all tables, columns, types, and constraints
✅ `backend/sample-data.json` demonstrates expected data structure
✅ Schema supports single-user MVP and is extensible for future multi-user/multi-board
✅ User has reviewed and approved the schema

---

## Part 6: Backend API Routes

**Objective:** Implement FastAPI routes to read and modify Kanban data. Create SQLite database automatically if missing. Comprehensive backend unit tests.

### Sub-steps (Checklist)

- [ ] Create `backend/db.py`
  - Initialize SQLite connection (file: `kanban.db` in backend root)
  - Create tables on first run if they don't exist
  - Provide helper functions: get_user(), get_board(), execute_query()
- [ ] Create `backend/models.py`
  - Pydantic models for request/response validation
  - BoardData, Column, Card, User models
- [ ] Create `backend/routes.py`
  - GET `/api/boards/<user_id>` - Fetch user's board with columns and cards
    - Returns full board state as JSON
  - POST `/api/cards` - Add new card to a column
    - Request: { column_id, title, details }
    - Response: { card_id, ... } or error
  - PUT `/api/cards/<card_id>` - Move card to different column or position
    - Request: { column_id, position }
    - Response: { success: true } or error
  - DELETE `/api/cards/<card_id>` - Delete card
    - Response: { success: true } or error
  - PUT `/api/columns/<column_id>` - Rename column
    - Request: { title }
    - Response: { success: true } or error
- [ ] Update `backend/main.py`
  - Import and register routes from routes.py
  - Initialize database on startup
- [ ] Seed database with demo data
  - Create user "user" with password (hashed? or plaintext for MVP)
  - Create one board with 5 columns and 8 cards
- [ ] Create `backend/tests/` directory
  - `test_db.py` - Database initialization and query tests
  - `test_routes.py` - API endpoint tests (mock or real SQLite in-memory)

### Tests

**Unit Tests (Backend):**
- Database initialization: tables are created on first run
- CRUD operations: create, read, update, delete cards and columns
- Card movement logic: same column reorder, cross-column move
- Column rename logic
- Error handling: card not found, column not found, etc.

**Integration Tests:**
- Full API flow: create board → add card → move card → rename column → delete card
- Data persistence: data survives app restart
- Concurrent operations: multiple API calls don't corrupt data

**Manual Tests (using curl or Postman):**
- GET `/api/boards/user` returns board with 5 columns and 8 cards
- POST `/api/cards` creates new card and returns it
- PUT `/api/cards/<id>` moves card successfully
- DELETE `/api/cards/<id>` removes card
- PUT `/api/columns/<id>` renames column

### Success Criteria

✅ SQLite database is created automatically on first run
✅ Demo user "user" and one board are seeded in database
✅ All CRUD endpoints work correctly
✅ Database persists data across app restarts
✅ All backend unit and integration tests pass
✅ API responses match Pydantic models (proper validation)
✅ Error handling for edge cases (404, invalid input, etc.)

---

## Part 7: Connect Frontend to Backend API

**Objective:** Replace in-memory state in frontend with API calls to backend. Implement fetching, creating, updating, and deleting cards via API. Comprehensive integration and e2e tests.

### Sub-steps (Checklist)

- [ ] Create `frontend/src/lib/api.ts`
  - Wrapper functions for all API endpoints
  - getBoard(userId) → BoardData
  - createCard(columnId, title, details) → Card
  - moveCard(cardId, columnId, position) → success
  - deleteCard(cardId) → success
  - renameColumn(columnId, title) → success
  - Error handling and retry logic (optional for MVP)
- [ ] Update `frontend/src/components/KanbanBoard.tsx`
  - On mount, fetch board from `/api/boards/user`
  - Add loading state while fetching
  - Replace all state mutations with API calls
  - handleAddCard calls api.createCard() instead of local state
  - handleDeleteCard calls api.deleteCard()
  - handleDragEnd calls api.moveCard()
  - handleRenameColumn calls api.renameColumn()
  - Refetch board or optimistically update UI after each mutation
- [ ] Add error handling
  - Display toast/alert on API errors
  - Retry failed requests (optional)
  - Graceful degradation if API is unavailable
- [ ] Create `frontend/src/lib/storage.ts` (if needed)
  - Track which user is logged in
  - Pass userId to all API calls
- [ ] Update login flow
  - Store user ID in localStorage after login (e.g., userId: "1")
  - Pass to getBoard() call
- [ ] Update authentication middleware (backend)
  - Add user authentication to routes (optional for MVP: hardcoded userId="1")
  - Or accept user_id as query param/header

### Tests

**Unit Tests (Frontend):**
- api.ts functions format requests correctly
- KanbanBoard component calls API on mount
- Mutations trigger correct API calls
- Error states display error messages

**Integration Tests:**
- Full flow: login → fetch board → add card → move card → logout
- Data persistence: card added via UI appears after refresh
- Concurrent operations: multiple cards can be added simultaneously

**E2E Tests (Playwright):**
- Login with "user"/"password"
- Kanban board loads and displays server data (not demo data)
- Drag card to different column → API called, UI updated, persists after refresh
- Add card → API called, card appears, persists after refresh
- Delete card → API called, card removed, persists after refresh
- Rename column → API called, title updates, persists after refresh
- Logout and login again → board state is exactly as left (persisted)

### Success Criteria

✅ Frontend fetches board from backend on load
✅ All card mutations (add, move, delete) call backend API
✅ Column rename calls backend API
✅ Data persists across page refreshes
✅ Data persists across logout/login
✅ Loading states display while fetching
✅ Error messages display on API failures
✅ All unit, integration, and e2e tests pass
✅ No console errors during normal usage

---

## Part 8: AI Connectivity (OpenRouter)

**Objective:** Verify OpenRouter API integration works. Test with a simple "2+2=?" query to confirm API connectivity and response handling.

### Sub-steps (Checklist)

- [ ] Create `backend/ai.py`
  - Import requests library
  - Load OPENROUTER_API_KEY from environment
  - Function: `call_ai(prompt: str, model: str = "openai/gpt-oss-20b:free") → str`
    - Make POST request to OpenRouter API endpoint
    - Send prompt and model name
    - Handle response and extract text
    - Handle errors (network, auth, rate limit, etc.)
- [ ] Add test endpoint to backend
  - GET `/api/ai-test` → calls `call_ai("2+2=?")` and returns response
  - This verifies connectivity without needing the full Kanban context yet
- [ ] Create `backend/tests/test_ai.py`
  - Mock OpenRouter API responses
  - Test call_ai() returns expected format
  - Test error handling (network error, auth error, etc.)
- [ ] Verify OPENROUTER_API_KEY is in `.env` file at project root

### Tests

**Unit Tests:**
- call_ai() with mocked API returns correct response format
- Error handling for various API failures

**Integration Tests (Live):**
- Call `/api/ai-test` endpoint
- Receive response from OpenRouter with answer to "2+2=?"
- Response format is valid JSON

**Manual Test:**
- Run backend
- curl `http://localhost:8000/api/ai-test`
- Receive response: `{ "response": "4" }` or similar

### Success Criteria

✅ OPENROUTER_API_KEY is loaded from .env without errors
✅ /api/ai-test endpoint makes successful API call to OpenRouter
✅ Receives valid response from AI model
✅ Response is parsed and returned as JSON
✅ Errors are handled gracefully (timeout, rate limit, auth failure, etc.)
✅ All unit and integration tests pass

---

## Part 9: AI with Kanban Context & Structured Outputs

**Objective:** Extend AI integration to send full Kanban board state + user question + conversation history. AI responds with Structured Outputs containing response text and optional Kanban updates (delta changes only). Comprehensive tests.

### Sub-steps (Checklist)

- [ ] Update `backend/ai.py`
  - Create structured output schema for AI response
    ```
    {
      "response": "Text reply to user",
      "kanban_update": {
        "action": "move_card" | "create_card" | "delete_card" | "rename_column" | null,
        "card_id": "...",
        "column_id": "...",
        "title": "...",
        "position": 0,
        "details": "..."
      }
    }
    ```
  - Function: `call_ai_with_kanban(board_state, user_question, conversation_history) → StructuredOutput`
    - Build prompt with full board JSON
    - Include recent conversation messages (last 5-10)
    - Send to OpenRouter with instructions to return JSON matching schema
    - Parse and validate response
- [ ] Create `backend/conversation.py`
  - Store conversation history in memory (for MVP single user)
  - Or in database if persistence needed
  - Keep last 10 messages for context
  - Clear history on logout
- [ ] Create new backend route
  - POST `/api/ai` (or GET `/api/chat`)
    - Request: { user_id, question }
    - Response: { response, kanban_update }
    - Validate kanban_update against current board state
    - If update is invalid, respond with error in text
    - If valid, don't apply it (frontend will handle if it chooses)
- [ ] Add validation logic
  - Check kanban_update.card_id exists
  - Check kanban_update.column_id exists
  - Check position is within valid range
  - Return error message if validation fails
- [ ] Create comprehensive tests

### Tests

**Unit Tests:**
- call_ai_with_kanban() parses response into StructuredOutput
- Structured output schema validation
- Conversation history management (add, retrieve recent)
- Invalid kanban_update detection and error generation

**Integration Tests:**
- Full AI flow: send question + board → receive response + optional update
- Response contains valid JSON with response text
- Kanban update (if present) is valid for the board state
- Invalid updates are rejected with error message
- Conversation history is maintained across calls

**Prompt Testing:**
- Prompt includes full board JSON structure
- Prompt includes recent conversation history
- AI instructions are clear about expected response format

**E2E Tests (Manual or Playwright):**
- POST to `/api/ai` with sample question and board
- Receive response with text and optional update
- Verify response text is natural language
- Verify update (if present) is syntactically valid

### Success Criteria

✅ Backend sends full Kanban board state to AI
✅ Recent conversation history is included (last 5-10 messages)
✅ AI responds with Structured Output matching schema
✅ Response contains user-facing text reply
✅ Optional kanban_update contains only delta changes, not full board
✅ Invalid kanban_updates are detected and reported
✅ Valid kanban_updates have all required fields
✅ Conversation history is maintained and cleared appropriately
✅ All unit, integration, and validation tests pass

---

## Part 10: AI Chat Sidebar UI

**Objective:** Add beautiful, fixed-width sidebar to frontend supporting full AI chat. Display conversation history. Allow AI to update Kanban via Structured Outputs. Animations on updates. Comprehensive tests.

### Sub-steps (Checklist)

- [ ] Create `frontend/src/components/AIChatSidebar.tsx`
  - Fixed-width sidebar (suggest 350-400px)
  - Positioned on right side or left (design choice)
  - Message list showing conversation history
    - User messages: right-aligned, purple/primary-blue color
    - AI messages: left-aligned, gray/navy color
  - Input field at bottom with send button
  - Loading state while waiting for AI response
  - Error display if API fails
- [ ] Create `frontend/src/components/ChatMessage.tsx`
  - Render individual message (user or AI)
  - Display timestamp (optional)
  - Syntax highlighting for JSON blocks in AI response (optional)
- [ ] Create `frontend/src/lib/chat.ts`
  - sendMessage(userId, question, boardState, conversationHistory) → StructuredOutput
  - Calls POST /api/ai on backend
  - Error handling and formatting
- [ ] Update `frontend/src/components/KanbanBoard.tsx`
  - Add AIChatSidebar component to layout
  - Pass board state to sidebar
  - Listen for kanban_update from AI response
  - Apply update to board if present (with optional optimistic UI)
  - Animate card movement when AI updates board
    - Toast/notification: "AI moved 'Task X' to 'Done'"
    - Card slides smoothly to new column
- [ ] Add conversation persistence (optional for MVP)
  - Store conversation in localStorage
  - Load on page load
- [ ] Styling with Tailwind
  - Use design system colors (purple for AI accent, blue for primary)
  - Rounded corners matching Kanban aesthetic
  - Shadow and backdrop blur for depth
  - Smooth transitions for messages and card updates
- [ ] Add animations
  - Message fade-in
  - Card move animation (CSS transform + transition)
  - Pulse or highlight on Kanban update
- [ ] Accessibility
  - ARIA labels for chat input, send button
  - Focus management
  - Keyboard shortcut to focus input (optional: Cmd+K)

### Tests

**Unit Tests:**
- AIChatSidebar component renders message list
- Chat input submits message on send
- Loading state displays while waiting for AI
- Error message displays on API failure
- sendMessage() formats request correctly

**Integration Tests:**
- Full chat flow: type message → send → receive response → display in UI
- Kanban update from AI response is applied to board
- Card animation plays when AI moves card
- Message history is maintained in component state
- Multiple messages back-and-forth work correctly

**E2E Tests (Playwright):**
- Sidebar is visible on right side of Kanban
- User can type message and click send button
- Message appears in chat history
- AI response appears after a delay
- If AI moves a card: card animates to new column
- If AI renames column: column title updates
- Refresh page: chat history persists (if localStorage used)
- Close sidebar and reopen: message history is intact
- Try message that AI doesn't update Kanban: just displays response
- Error message displays if API fails

**Visual/Animation Tests:**
- Messages fade in smoothly
- Cards animate smoothly when moved
- Notification toast appears with Kanban update
- No jarring layout shifts (sidebar shouldn't cause CLS)

### Success Criteria

✅ AI Chat sidebar is visible and fixed-width
✅ User can type and send messages
✅ Messages display in chronological order
✅ AI responses appear with user-facing text
✅ Kanban updates from AI are applied to board
✅ Card animations play smoothly on board updates
✅ Toast/notification appears when AI updates board
✅ Conversation history persists (localStorage or session)
✅ Error handling for network/API failures
✅ Sidebar styling matches design system
✅ Animations are smooth and performant
✅ All component, integration, and e2e tests pass
✅ No console errors or warnings during usage

---

## Testing Summary

### Test Pyramid

```
        /\
       /  \  E2E Tests (Playwright)
      /    \ - Full user workflows
     /      \ - Cross-browser testing
    /--------\
   /          \  Integration Tests
  /            \ - Component + API combos
 /              \ - Full feature flows
/----------------\
/                  \ Unit Tests (Vitest + Backend pytest)
/                    \ - Individual functions
/                      \ - Component behavior
/                        \ - API endpoints
```

### Test Coverage Goals

- **Unit Tests**: 80%+ coverage
- **Integration Tests**: Cover all major user flows
- **E2E Tests**: Happy path for all 10 parts

### Running Tests

```bash
# Frontend unit tests
npm run test:unit
npm run test:unit:watch

# Frontend E2E tests
npm run test:e2e

# Backend unit tests (Python)
cd backend && python -m pytest

# All tests
npm run test:all && cd ../backend && python -m pytest
```

---

## Definitions of Done

A part is considered **DONE** when:

1. ✅ All sub-steps checklist items are completed
2. ✅ Unit tests pass with >80% coverage
3. ✅ Integration tests cover the feature flow
4. ✅ E2E tests verify user-facing behavior
5. ✅ No console errors or warnings
6. ✅ Code is committed with clear commit messages
7. ✅ Documentation is updated (if needed)
8. ✅ User/stakeholder has tested and approved (for Parts 1, 5, final part)

---

## Notes

- **Simplicity First**: Each part should be minimal and focused. Don't add extra features.
- **Error Handling**: Graceful degradation on failures (network, auth, etc.)
- **Data Persistence**: Verify data survives app restart after each relevant part
- **User Experience**: Loading states, error messages, animations where helpful
- **Documentation**: Keep README minimal. Detailed docs in `docs/` directory.