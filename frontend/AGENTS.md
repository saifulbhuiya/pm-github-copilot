# Frontend Codebase Documentation

## Overview

A Next.js 16+ frontend for the Kanban Project Management MVP. Currently a pure frontend demo (no backend) using React 19, TypeScript, Tailwind CSS, and dnd-kit for drag-and-drop. All data is in-memory state.

## Tech Stack

- **Framework**: Next.js 16.1.6 with App Router
- **UI Library**: React 19.2.3
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 4 with PostCSS
- **Drag & Drop**: dnd-kit 6 (@dnd-kit/core, @dnd-kit/sortable, @dnd-kit/utilities)
- **Utilities**: clsx for classname concatenation
- **Testing**: Vitest 3 (unit), Playwright 1.58 (e2e)
- **Linting**: ESLint 9

## Directory Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root layout wrapper
│   │   ├── page.tsx             # Home page (renders KanbanBoard)
│   │   └── globals.css          # Global styles, Tailwind config, CSS variables
│   ├── components/
│   │   ├── KanbanBoard.tsx       # Main component, state & drag orchestration
│   │   ├── KanbanColumn.tsx      # Column component with rename form
│   │   ├── KanbanCard.tsx        # Individual card (editable details)
│   │   ├── KanbanCardPreview.tsx # Dragging preview overlay
│   │   ├── NewCardForm.tsx       # Add card form
│   │   └── *.test.tsx            # Unit tests for components
│   ├── lib/
│   │   ├── kanban.ts            # Core Kanban logic & data structures
│   │   ├── kanban.test.ts        # Logic unit tests
│   │   └── kanban.ts             # No other lib files currently
│   └── test/
│       └── (support files if any)
├── tests/                        # E2E test files (Playwright)
├── public/                       # Static assets
├── package.json                  # Dependencies & scripts
├── next.config.ts               # Next.js configuration
├── tsconfig.json                # TypeScript configuration
├── vitest.config.ts             # Vitest configuration
├── playwright.config.ts         # Playwright configuration
├── tailwind.config.js           # Tailwind configuration (if separate)
└── postcss.config.mjs           # PostCSS configuration
```

## Core Data Structures

### Board Model (lib/kanban.ts)

```typescript
type Card = {
  id: string;       // e.g., "card-abc123def456"
  title: string;    // Card heading
  details: string;  // Card description/body
};

type Column = {
  id: string;       // e.g., "col-backlog"
  title: string;    // Editable column name
  cardIds: string[]; // Array of card IDs in this column
};

type BoardData = {
  columns: Column[];           // Fixed 5 columns (Backlog, Discovery, In Progress, Review, Done)
  cards: Record<string, Card>; // Card lookup by ID
};
```

## Component Architecture

### KanbanBoard (Container Component)

**Responsibilities:**
- Holds all board state (columns and cards)
- Manages drag-and-drop via DndContext
- Routes drag events to column/card move logic
- Provides handlers to children for rename, add, delete operations
- Renders header with board title and column overview
- Renders column grid and DragOverlay

**Key Methods:**
- `handleDragStart()` - Tracks which card is being dragged
- `handleDragEnd()` - Calls moveCard() to reorder/move cards
- `handleRenameColumn()` - Updates column title
- `handleAddCard()` - Creates new card with ID and adds to column
- `handleDeleteCard()` - Removes card from board and column

**State:**
- `board: BoardData` - Current board configuration and cards
- `activeCardId: string | null` - Currently dragged card for overlay

### KanbanColumn (Presentational Component)

**Responsibilities:**
- Renders a single column with header and card list
- Provides rename input for column title
- Renders NewCardForm for adding cards
- Uses SortableContext from dnd-kit for droppability
- Shows card count in header

**Props:**
- `column: Column`
- `cards: Card[]`
- `onRename: (columnId, title) => void`
- `onAddCard: (columnId, title, details) => void`
- `onDeleteCard: (columnId, cardId) => void`

### KanbanCard (Card Display)

**Responsibilities:**
- Renders card title and details
- Provides delete button
- Uses useSortable hook to enable drag

**Props:**
- `card: Card`
- `onDelete: (cardId) => void`

### KanbanCardPreview (Drag Preview)

**Responsibilities:**
- Renders a styled copy of the card during drag for DragOverlay

**Props:**
- `card: Card`

### NewCardForm (Form Component)

**Responsibilities:**
- Provides inputs for title and details
- Submits new card to parent via onAdd callback
- Clears form after submission

**Props:**
- `onAdd: (title, details) => void`

## Styling Approach

### Design System (CSS Variables in globals.css)

```css
--accent-yellow: #ecad0a
--primary-blue: #209dd7
--secondary-purple: #753991
--navy-dark: #032147
--gray-text: #888888
--surface: #f7f8fb
--surface-strong: #ffffff
--stroke: rgba(3, 33, 71, 0.08)
--shadow: 0 18px 40px rgba(3, 33, 71, 0.12)
```

### Tailwind Patterns

- **Spacing**: gap-6, px-6, py-4 (6=24px default)
- **Colors**: `text-[var(--navy-dark)]`, `bg-[var(--primary-blue)]`
- **Shadows**: `shadow-[var(--shadow)]` for card elevation
- **Borders**: `border border-[var(--stroke)]` for subtle dividers
- **Rounded**: `rounded-[32px]` (large), `rounded-2xl` (medium), `rounded-full` (pills)
- **Gradients**: Radial gradient backgrounds for visual depth

### Drag & Drop Styling

- Active drag uses opacity or transform
- DragOverlay renders floating preview during drag
- No visual feedback on droppable areas (smooth UX)

## Key Utilities (lib/kanban.ts)

### createId(prefix: string)
Generates unique IDs using random + timestamp:
```typescript
export const createId = (prefix: string) => {
  const randomPart = Math.random().toString(36).slice(2, 8);
  const timePart = Date.now().toString(36);
  return `${prefix}-${randomPart}${timePart}`;
};
// Returns: "card-abc123def456" or "col-xyz789ghi012"
```

### moveCard(columns, activeId, overId)
Handles all drag-drop reordering logic:
- Same column reorder (change position of card in same column)
- Cross-column move (move card to different column)
- Drop on column vs drop on card (different insertion logic)
- Returns new columns array (immutable)

### initialData
Hardcoded demo board with 5 columns and 8 sample cards.

## Testing Strategy

### Unit Tests (Vitest)

**Coverage Areas:**
1. **kanban.ts logic**
   - `moveCard()` with various scenarios (same column, cross-column, drop-on-column, drop-on-card)
   - `createId()` uniqueness and format
   - Initial data structure validation

2. **Component unit tests**
   - KanbanBoard state updates (rename, add, delete)
   - Column rename functionality
   - Card add/delete functionality
   - Props pass-through and callbacks

**Run:** `npm run test:unit`
**Watch:** `npm run test:unit:watch`
**Coverage:** `npm run test:unit -- --coverage`

### E2E Tests (Playwright)

**Coverage Areas:**
1. **Drag and drop**
   - Drag card within same column (reorder)
   - Drag card to different column
   - Drag to empty column
   - Drag to top/bottom of column

2. **Interactions**
   - Click to rename column
   - Add new card via form
   - Delete card
   - See updated board state

3. **Visual**
   - Header renders with title and column list
   - 5 columns visible
   - Cards display correctly

**Run:** `npm run test:e2e`
**All tests:** `npm run test:all`

## Build & Runtime

### Scripts

```json
{
  "dev": "next dev",           // Development server on :3000
  "build": "next build",       // Production build to .next/
  "start": "next start",       // Serve built app
  "lint": "eslint",            // Lint check
  "test": "vitest run",        // Run all Vitest tests
  "test:unit": "vitest run",   // Run unit tests only
  "test:unit:watch": "vitest", // Watch unit tests
  "test:e2e": "playwright test", // Run Playwright tests
  "test:all": "npm run test:unit && npm run test:e2e"
}
```

### Development Workflow

1. `npm install` - Install dependencies
2. `npm run dev` - Start dev server (http://localhost:3000)
3. `npm run test:unit:watch` - Watch tests in parallel terminal
4. Edit components, see changes hot-reload and tests re-run

### Production Build

1. `npm run build` - Creates .next/ with optimized bundle
2. `npm run start` - Serves production bundle (http://localhost:3000)

## Integration Points (Future)

The following are designed for easy backend integration:

1. **State fetching**: Replace `useState` with API call in KanbanBoard
2. **Persistence**: Add POST/PUT/DELETE handlers to mutations (handleAddCard, handleDeleteCard, handleRenameColumn, handleDragEnd)
3. **Auth redirect**: Add auth check in layout.tsx or page.tsx
4. **API client**: Create lib/api.ts with fetch wrappers for backend routes

## Current Limitations

1. All state is in-memory (lost on refresh)
2. No user authentication
3. No backend integration
4. Only one board (hardcoded data)
5. No card detail editing UI (but details exist in model)
6. No API error handling or loading states
7. No conversation history or AI features

## Next Steps (Per PLAN.md)

- Part 2-4: Add Docker, backend scaffolding, login screen
- Part 5-6: Add database and API routes
- Part 7: Connect frontend to backend API
- Part 8-10: Integrate AI chat sidebar with LLM-driven updates
