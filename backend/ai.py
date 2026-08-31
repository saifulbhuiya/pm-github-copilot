import json
import os
import re
from typing import Optional

import httpx

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-20b:free")
COLUMN_NAME_MAP = {
    "backlog": "Backlog",
    "discovery": "Discovery",
    "in progress": "In Progress",
    "in_progress": "In Progress",
    "review": "Review",
    "done": "Done",
}


def _normalize(value: Optional[str]) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def _find_column(board_state: dict, label: Optional[str]):
    if not label:
        return None
    normalized = _normalize(label)
    for column in board_state["columns"]:
        if _normalize(column["title"]) == normalized:
            return column
    for column in board_state["columns"]:
        if normalized in _normalize(column["title"]):
            return column
    return None


def _find_card(board_state: dict, label: Optional[str]):
    if not label:
        return None
    normalized = _normalize(label)
    for card_id, card in board_state["cards"].items():
        if _normalize(card.get("title")) == normalized:
            return card_id, card
    for card_id, card in board_state["cards"].items():
        if normalized in _normalize(card.get("title")):
            return card_id, card
    return None


def _fallback_parse(board_state: dict, user_message: str) -> dict:
    message = user_message.strip()
    action = "create"
    lowered = message.lower()

    if any(word in lowered for word in ["move", "drag", "send", "put", "shift"]):
        action = "move"
    elif any(word in lowered for word in ["delete", "remove", "drop"]):
        action = "delete"
    elif any(word in lowered for word in ["rename", "retitle"]):
        action = "rename"

    cards = []
    if action == "create":
        remaining = re.sub(r"^(create|add|new|make)\s+", "", message, flags=re.I).strip()
        if " in " in remaining.lower():
            remaining = re.split(r"\s+in\s+", remaining, maxsplit=1, flags=re.I)[0]
        if " to " in remaining.lower():
            remaining = re.split(r"\s+to\s+", remaining, maxsplit=1, flags=re.I)[0]
        column_label = "Backlog"
        match = re.search(r"\s+(in|to|into)\s+([a-zA-Z ]+)", message, flags=re.I)
        if match:
            column_label = match.group(2).strip()
        title = remaining or "New task"
        cards.append({
            "id": None,
            "title": title,
            "details": "Created via AI request",
            "column": column_label,
            "position": 0,
        })
    elif action == "move":
        match = re.search(r"(?:move|drag|send|put|shift)\s+(.+?)(?:\s+(?:to|into|in))\s+(.+)$", message, flags=re.I)
        if match:
            title = match.group(1).strip()
            column_label = match.group(2).strip()
        else:
            title = message
            column_label = "Backlog"
        cards.append({
            "id": None,
            "title": title,
            "details": "",
            "column": column_label,
            "position": 0,
        })
    elif action == "delete":
        title = re.sub(r"^(delete|remove|drop)\s+", "", message, flags=re.I).strip()
        cards.append({
            "id": None,
            "title": title,
            "details": "",
            "column": "Backlog",
            "position": 0,
        })
    elif action == "rename":
        cards.append({
            "id": None,
            "title": message,
            "details": "",
            "column": "Backlog",
            "position": 0,
        })

    return {"action": action, "cards": cards}


async def call_ai(prompt: str, system: Optional[str] = None, json_schema: Optional[dict] = None) -> str:
    """Call the OpenRouter API and return the response content."""
    api_key = os.getenv("OPENROUTER_API_KEY") or OPENROUTER_API_KEY
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    model = os.getenv("OPENROUTER_MODEL", MODEL)
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
    }

    if json_schema:
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "response",
                "schema": json_schema,
            },
        }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            json=payload,
            headers=headers,
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


async def parse_ai_command(board_state: dict, user_message: str) -> dict:
    """Parse a natural-language request into a structured board action."""
    api_key = os.getenv("OPENROUTER_API_KEY") or OPENROUTER_API_KEY
    if not api_key:
        return _fallback_parse(board_state, user_message)

    system_prompt = """You are a Kanban board assistant. Respond with JSON only:
{
  "action": "create" | "move" | "delete" | "rename" | "multi",
  "cards": [
    {
      "id": "optional_id",
      "title": "card title",
      "details": "card description",
      "column": "Backlog|Discovery|In Progress|Review|Done",
      "position": 0
    }
  ]
}

Use "multi" when there are multiple tasks in one request."""

    board_context = f"Current board state:\nColumns: {', '.join(col['title'] for col in board_state['columns'])}\nCards: {json.dumps(board_state['cards'], ensure_ascii=False)}"
    full_prompt = f"{board_context}\n\nUser request: {user_message}"

    json_schema = {
        "type": "object",
        "properties": {
            "action": {"type": "string"},
            "cards": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": ["string", "null"]},
                        "title": {"type": "string"},
                        "details": {"type": "string"},
                        "column": {"type": "string"},
                        "position": {"type": "integer"},
                    },
                    "required": ["title", "column"],
                },
            },
        },
        "required": ["action", "cards"],
    }

    try:
        response_text = await call_ai(full_prompt, system_prompt, json_schema)
        return json.loads(response_text)
    except Exception:
        return _fallback_parse(board_state, user_message)


def execute_ai_command(board_state: dict, command: dict):
    """Apply the structured AI command to the real board state."""
    from db import create_card, move_card, delete_card, rename_column

    diff = []
    applied = []
    action = command.get("action", "")

    for item in command.get("cards", []):
        title = (item.get("title") or "").strip()
        if not title:
            continue

        column_label = item.get("column") or "Backlog"
        column = _find_column(board_state, column_label)

        if action in {"create", "update", "multi"} and item.get("id") is None:
            if not column:
                continue
            card_id = create_card(int(column["id"].replace("col-", "")), title, item.get("details") or "")
            applied.append({"id": str(card_id), "title": title, "column": column["title"]})
            diff.append({"kind": "added", "text": f"+ {title} -> {column['title']}"})
            continue

        if action in {"move", "multi"}:
            match = _find_card(board_state, item.get("id") or title)
            if not match:
                continue
            card_id, current_card = match
            if not column:
                continue
            position = int(item.get("position", 0) or 0)
            move_card(1, int(card_id), int(column["id"].replace("col-", "")), position)
            applied.append({
                "id": str(card_id),
                "title": current_card.get("title"),
                "from": "current",
                "to": column["title"],
            })
            diff.append({"kind": "modified", "text": f"~ {current_card.get('title')} -> {column['title']}"})
            continue

        if action in {"delete", "multi"}:
            match = _find_card(board_state, item.get("id") or title)
            if match:
                card_id, current_card = match
                delete_card(int(card_id))
                applied.append({
                    "id": str(card_id),
                    "title": current_card.get("title"),
                    "deleted": True,
                })
                diff.append({"kind": "removed", "text": f"- {current_card.get('title')}"})
                continue

        if action in {"rename"}:
            if column and title:
                rename_column(int(column["id"].replace("col-", "")), title)
                applied.append({
                    "id": column["id"],
                    "old_title": column["title"],
                    "title": title,
                })
                diff.append({"kind": "modified", "text": f"~ Column: {column['title']} -> {title}"})
                continue

    if not diff:
        return {
            "action": command.get("action", "noop"),
            "cards": [],
            "diff": [{"kind": "modified", "text": "No matching board updates were applied."}],
            "summary": "No matching board updates were applied.",
            "applied": False,
        }

    summary = "Updated the board." if command.get("action") else "Processed your request."
    if action == "create":
        summary = f"Created {len(applied)} task(s)."
    elif action == "move":
        summary = f"Moved {len(applied)} task(s) to a new stage."
    elif action == "delete":
        summary = f"Deleted {len(applied)} task(s)."
    elif action == "rename":
        summary = f"Renamed column to {title}."

    return {
        "action": action or "update",
        "cards": applied,
        "diff": diff,
        "summary": summary,
        "applied": True,
    }
