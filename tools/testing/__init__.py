"""
🧪 TESTING TOOLS

Unit, integration, and E2E testing tools.
"""

import json
from crewai.tools import tool


@tool("generate_pytest")
def generate_pytest(name: str, path: str = "workspace/tests/unit") -> str:
    """Generate pytest test."""
    content = f'''import pytest

def test_{name.replace("-", "_")}():
    """Test for {name}."""
    assert True
'''
    file_path = f"{path}/{name}.py"
    import os
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)
    return f"Test created: {file_path}"


@tool("generate_jest")
def generate_jest(name: str, path: str = "workspace/tests") -> str:
    """Generate Jest test."""
    content = f'''describe("{name}", () => {{
  it("should work", () => {{
    expect(true).toBe(true);
  }});
}});
'''
    file_path = f"{path}/{name}.test.ts"
    import os
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)
    return f"Test created: {file_path}"


@tool("generate_playwright")
def generate_playwright(name: str, path: str = "workspace/tests/e2e") -> str:
    """Generate Playwright test."""
    content = f'''import {{ test, expect }} from "@playwright/test";

test("{name}", async ({{ page }}) => {{
  await page.goto("/");
  await expect(page).toHaveTitle(/My App/);
}});
'''
    file_path = f"{path}/{name}.spec.ts"
    import os
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)
    return f"Test created: {file_path}"


@tool("save_playwright_config")
def save_playwright_config(path: str = "workspace/playwright.config.ts") -> str:
    """Generate Playwright config."""
    content = '''import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  reporter: "html",
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
  ],
});
'''
    with open(path, "w") as f:
        f.write(content)
    return f"Playwright config saved: {path}"


__all__ = ["generate_pytest", "generate_jest", "generate_playwright", "save_playwright_config"]