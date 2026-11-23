---
name: browser-qa
description: Use when a task changes a web UI, listing/review workflow, browser behavior, responsive layout, or user interaction. Verify actual user paths and visible quality, not only unit tests.
---

# Browser and user-interface QA

- Inspect the existing test harness and application entrypoints. Prefer existing Playwright/browser tests before installing new tooling.
- Run the real application in the permitted environment. Check happy path, empty/error states, desktop and mobile viewport, accessibility basics, keyboard flow, console errors, network failures, and persistence where relevant.
- Compare the produced UI against acceptance criteria and any authorized public reference designs; do not copy restricted content, scrape prohibited sites, or expose private browser sessions.
- If browser instrumentation is unavailable or permissions are not granted, report the exact untested scenarios rather than fabricating screenshots or claims.
- Distinguish mocked data from real integrations, and local draft from publication. Protect private evidence, PII, credentials and media.
- Report concrete before/after findings, screenshots/test IDs where permitted, exact commands, failed cases, and remaining risk.
- Browser developer/CDP access is high-trust; do not enable broad access or log private browser data without explicit permission.
