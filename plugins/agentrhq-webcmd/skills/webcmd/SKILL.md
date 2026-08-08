---
name: webcmd
description: Use AgentRHQ Webcmd to discover site adapters, research websites, invoke deterministic site commands, or drive a browser as a fallback.
---

# AgentRHQ Webcmd

Use this skill for live web research, website data retrieval, and browser automation tasks. Start by inspecting Webcmd's available commands and adapters, then prefer a deterministic adapter command when one covers the requested website action.

## Workflow

1. Discover the matching adapter and its supported commands.
2. Use the adapter for read or write actions with only the parameters required.
3. If no adapter covers the task, use Webcmd browser automation and verify the visible page state before reporting success.
4. Clearly distinguish information retrieved from a website from assumptions or inferences.

## Safety

Ask for confirmation before external side effects such as sending messages, submitting forms, publishing content, deleting data, or making purchases. Do not expose credentials, cookies, access tokens, or other sensitive page data.

## Fallback

If the `webcmd` executable is not available, explain that the AgentRHQ Webcmd package must be installed and configured in the current environment before this skill can complete live web tasks.
