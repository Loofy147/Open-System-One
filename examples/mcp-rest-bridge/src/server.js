import { McpServer } from "@modelcontextprotocol/server";
import * as z from "zod/v4";

export function buildServer({
  apiBaseUrl,
  apiKey = undefined,
  fetchImpl = globalThis.fetch,
} = {}) {
  if (!apiBaseUrl) {
    throw new Error("API_BASE_URL is required");
  }

  const base = new URL(apiBaseUrl);
  if (base.protocol !== "http:" && base.protocol !== "https:") {
    throw new Error("API_BASE_URL must use http or https");
  }

  if (typeof fetchImpl !== "function") {
    throw new Error("fetchImpl must be a function");
  }

  const server = new McpServer({
    name: "rest-bridge-demo",
    version: "0.1.0",
  });

  server.registerTool(
    "get_resource",
    {
      title: "Get REST resource",
      description: "Fetch one resource from the configured REST API.",
      inputSchema: z.object({
        id: z.string().min(1).max(256),
      }),
      annotations: {
        readOnlyHint: true,
        openWorldHint: true,
      },
    },
    async ({ id }) => {
      const baseUrl = base.endsWith("/") ? base : new URL(base.href + "/");
      const url = new URL("resources/" + encodeURIComponent(id), baseUrl);

      const headers = { accept: "application/json" };
      if (apiKey) {
        headers.authorization = "Bearer " + apiKey;
      }

      const response = await fetchImpl(url, { method: "GET", headers });
      const body = await response.text();

      if (!response.ok) {
        return {
          content: [
            {
              type: "text",
              text: "REST API error " + response.status + ": " + body.slice(0, 2000),
            },
          ],
          isError: true,
        };
      }

      let parsed;
      try {
        parsed = JSON.parse(body);
      } catch {
        return {
          content: [
            {
              type: "text",
              text: "REST API returned a non-JSON response",
            },
          ],
          isError: true,
        };
      }

      return {
        content: [{ type: "text", text: JSON.stringify(parsed) }],
        structuredContent: parsed,
      };
    },
  );

  return server;
}
