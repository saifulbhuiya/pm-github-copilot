import os
import json
import httpx
from typing import Optional

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "openai/gpt-4o-mini"  # Using a free/fast model for MVP

async def call_ai(prompt: str, system: Optional[str] = None, json_schema: Optional[dict] = None) -> str:
    """Call OpenRouter API and return response text"""
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not set")
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
    }
    
    # Add JSON schema if provided for structured outputs
    if json_schema:
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "response",
                "schema": json_schema,
            }
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
    """Parse AI response to determine actions (create, move, delete, rename cards)"""
    
    system_prompt = """You are a Kanban board assistant. Respond with a JSON object containing:
{
  "action": "create" | "move" | "delete" | "rename" | "update" | "multi",
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

For multi-action responses, use "multi" and include multiple operations."""
    
    board_context = f"""Current board state:
Columns: {', '.join([col['title'] for col in board_state['columns']])}
Cards per column: {json.dumps({col['title']: len(col.get('cardIds', [])) for col in board_state['columns']})}"""
    
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
                    }
                }
            }
        },
        "required": ["action", "cards"]
    }
    
    response_text = await call_ai(full_prompt, system_prompt, json_schema)
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {
            "action": "error",
            "message": "Failed to parse AI response",
            "raw": response_text
        }
