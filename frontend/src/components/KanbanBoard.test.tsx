import { render, screen, within, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi, beforeEach, describe, it, expect } from "vitest";
import { KanbanBoard } from "@/components/KanbanBoard";
import { initialData } from "@/lib/kanban";
import * as api from "@/lib/api";

vi.mock("@/lib/api", () => ({
  getBoard: vi.fn(),
  createCard: vi.fn().mockResolvedValue({ id: "card-new", title: "New card", details: "Notes" }),
  moveCard: vi.fn().mockResolvedValue({ success: true }),
  deleteCard: vi.fn().mockResolvedValue({ success: true }),
  renameColumn: vi.fn().mockResolvedValue({ success: true }),
}));

const getFirstColumn = async () => {
  const columns = await screen.findAllByTestId(/column-/i);
  return columns[0];
};

describe("KanbanBoard", () => {
  beforeEach(() => {
    vi.mocked(api.getBoard).mockResolvedValue(JSON.parse(JSON.stringify(initialData)));
  });

  it("renders five columns", async () => {
    render(<KanbanBoard />);
    const columns = await screen.findAllByTestId(/column-/i);
    expect(columns).toHaveLength(5);
  });

  it("renames a column", async () => {
    render(<KanbanBoard />);
    const column = await getFirstColumn();
    const input = within(column).getByLabelText("Column title");
    await userEvent.clear(input);
    await userEvent.type(input, "New Name");
    expect(input).toHaveValue("New Name");
  });

  it("adds and removes a card", async () => {
    render(<KanbanBoard />);
    const column = await getFirstColumn();
    const addButton = within(column).getByRole("button", {
      name: /add a card/i,
    });
    await userEvent.click(addButton);

    const titleInput = within(column).getByPlaceholderText(/card title/i);
    await userEvent.type(titleInput, "New card");
    const detailsInput = within(column).getByPlaceholderText(/details/i);
    await userEvent.type(detailsInput, "Notes");

    await userEvent.click(within(column).getByRole("button", { name: /add card/i }));

    await waitFor(() => {
      expect(within(column).getByText("New card")).toBeInTheDocument();
    });

    const deleteButton = within(column).getByRole("button", {
      name: /delete new card/i,
    });
    await userEvent.click(deleteButton);

    await waitFor(() => {
      expect(within(column).queryByText("New card")).not.toBeInTheDocument();
    });
  });
});
