import { test, expect } from "@playwright/test";

test.describe("Auth Flow", () => {
  test("login page shows connect button", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText("GrowPlant")).toBeVisible();
    await expect(page.getByText("Connect with GitHub")).toBeVisible();
  });

  test("redirects to GitHub OAuth on connect", async ({ page }) => {
    await page.goto("/");
    await page.getByText("Connect with GitHub").click();
    // Should leave our app to GitHub
    await expect(page).not.toHaveURL("/");
  });
});
