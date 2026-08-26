# Architecture

## B1 — WebMCP vertical slice

This file currently documents only the volatile runtime contract needed by the B1 spike. It
does not define Jorbit's production architecture.

### Target runtime

- Latest ChatGPT desktop app, using its built-in browser with site tools enabled.
- GPT-5.6 Sol or GPT-5.6 Terra. GPT-5.6 Luna currently has WebMCP disabled.
- Site tools are not currently available in Enterprise or Edu workspaces and remain subject
  to rollout availability.
- Vercel provides the required secure HTTPS context.

### API contract verified 2026-08-26

The current imperative API is `document.modelContext.registerTool(tool, options)`. The spike
registers `update_test_state` with `name`, `title`, `description`, an empty JSON `inputSchema`,
and an async `execute` callback. It passes an `AbortSignal` in `options`; aborting that signal
unregisters the tool when the React component unmounts.

Sources:

- https://learn.chatgpt.com/docs/webmcp
- https://webmachinelearning.github.io/webmcp/

