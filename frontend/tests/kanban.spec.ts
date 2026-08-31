import { expect, test } from "@playwright/test";

const login = async (page: any) => {
  await page.goto("/");
  await page.getByPlaceholder("user").fill("user");
  await page.getByPlaceholder("password").fill("password");
  await page.getByRole("button", { name: "Sign In" }).click();
  await expect(page.getByRole("heading", { name: "Kanban Studio" })).toBeVisible();
};

test("shows login screen and handles invalid credentials", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("button", { name: "Sign In" })).toBeVisible();
  await page.getByPlaceholder("user").fill("wronguser");
  await page.getByPlaceholder("password").fill("wrongpass");
  await page.getByRole("button", { name: "Sign In" }).click();
  await expect(page.getByText("Invalid username or password")).toBeVisible();
});

test("loads the kanban board after login", async ({ page }) => {
  await login(page);
  await expect(page.locator('[data-testid^="column-"]')).toHaveCount(5);
  await expect(page.getByText("AI Assistant")).toBeVisible();
});

test("adds a card to a column", async ({ page }) => {
  await login(page);
  const firstColumn = page.locator('[data-testid^="column-"]').first();
  await firstColumn.getByRole("button", { name: /add a card/i }).click();
  await firstColumn.getByPlaceholder("Card title").fill("Playwright card");
  await firstColumn.getByPlaceholder("Details").fill("Added via e2e.");
  await firstColumn.getByRole("button", { name: /add card/i }).click();
  await expect(firstColumn.getByText("Playwright card")).toBeVisible();
});

test("logs out cleanly", async ({ page }) => {
  await login(page);
  await page.getByRole("button", { name: "Logout" }).click();
  await expect(page.getByRole("button", { name: "Sign In" })).toBeVisible();
});

