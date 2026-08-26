"use client";

import { useEffect, useState } from "react";

type ModelContext = {
  registerTool: (
    tool: {
      name: string;
      title: string;
      description: string;
      inputSchema: object;
      execute: () => Promise<object>;
    },
    options?: { signal?: AbortSignal },
  ) => Promise<void>;
};

type Status = "checking" | "waiting" | "success" | "unsupported" | "error";

const messages: Record<Status, string> = {
  checking: "Checking WebMCP support...",
  waiting: "Waiting for agent...",
  success: "WebMCP tool invoked successfully",
  unsupported: "WebMCP is not available in this browser.",
  error: "The WebMCP tool could not be registered.",
};

export default function Home() {
  const [status, setStatus] = useState<Status>("checking");
  const [viewport, setViewport] = useState("");

  // B1, second measurement: the target runtime's real viewport. Read on the page
  // itself because the ChatGPT built-in browser exposes no devtools.
  useEffect(() => {
    const measure = () =>
      setViewport(
        `${window.innerWidth} x ${window.innerHeight} css px @ dpr ${window.devicePixelRatio}`,
      );
    measure();
    window.addEventListener("resize", measure);
    return () => window.removeEventListener("resize", measure);
  }, []);

  useEffect(() => {
    const modelContext = (document as Document & { modelContext?: ModelContext }).modelContext;

    if (!modelContext) {
      setStatus("unsupported");
      return;
    }

    const registration = new AbortController();

    void modelContext
      .registerTool(
        {
          name: "update_test_state",
          title: "Update test state",
          description:
            "Verify the Jorbit WebMCP connection by changing the visible page state.",
          inputSchema: {
            type: "object",
            properties: {},
            additionalProperties: false,
          },
          execute: async () => {
            setStatus("success");
            return {
              success: true,
              message: "WebMCP tool invoked successfully",
            };
          },
        },
        { signal: registration.signal },
      )
      .then(() => setStatus("waiting"))
      .catch(() => {
        if (!registration.signal.aborted) setStatus("error");
      });

    return () => registration.abort();
  }, []);

  return (
    <main>
      <section className={status} aria-live="polite">
        <p>Jorbit WebMCP vertical slice</p>
        <h1>{messages[status]}</h1>
        <small>Tool: update_test_state</small>
        <small className="viewport">Viewport: {viewport || "measuring..."}</small>
      </section>
    </main>
  );
}

