export async function getBoard() {
  const response = await fetch("/api/boards/user");
  if (!response.ok) throw new Error("Failed to fetch board");
  return response.json();
}

export async function createCard(columnId: number, title: string, details: string) {
  const response = await fetch("/api/cards", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ column_id: columnId, title, details }),
  });
  if (!response.ok) throw new Error("Failed to create card");
  return response.json();
}

export async function moveCard(cardId: number, columnId: number, position: number) {
  const response = await fetch(`/api/cards/${cardId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ column_id: columnId, position }),
  });
  if (!response.ok) throw new Error("Failed to move card");
  return response.json();
}

export async function deleteCard(cardId: number) {
  const response = await fetch(`/api/cards/${cardId}`, { method: "DELETE" });
  if (!response.ok) throw new Error("Failed to delete card");
  return response.json();
}

export async function renameColumn(columnId: number, title: string) {
  const response = await fetch(`/api/columns/${columnId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  if (!response.ok) throw new Error("Failed to rename column");
  return response.json();
}
