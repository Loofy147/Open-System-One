import test from "node:test";
import assert from "node:assert/strict";

import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";
import { createMcpHandler } from "@modelcontextprotocol/server";
import { buildServer } from "../src/server.js";

function mockRestFetch(expectedUrl, expectedAuth, payload) {
  return async (url, init) => {
    assert.equal(String(url), expectedUrl);
    assert.equal(init.method, "GET");
    assert.equal(init.headers.accept, "application/json");
    assert.equal(init.headers.authorization, "Bearer " + expectedAuth);

    return new Response(JSON.stringify(payload), {
      status: 200,
      headers: { "content-type": "application/json" },
    });
  };
}

test("modern MCP HTTP request reaches REST API and returns structured data", async () => {
  const payload = { id: "abc-123", status: "ready", amount: 42 };
  const apiUrl = "https://api.example.test/resources/abc-123";
  const restFetch = mockRestFetch(apiUrl, "demo-key", payload);

  const handler = createMcpHandler(() =>
    buildServer({
      apiBaseUrl: "https://api.example.test",
      apiKey: "demo-key",
      fetchImpl: restFetch,
    }),
  );

  const client = new Client({
    name: "integration-test-client",
    version: "0.1.0",
  });

  const transport = new StreamableHTTPClientTransport(
    new URL("http://mcp.example.test/mcp"),
    {
      fetch: (url, init) => handler.fetch(new Request(url, init)),
    },
  );

  await client.connect(transport);

  const tools = await client.listTools();
  assert.equal(tools.tools.length, 1);
  assert.equal(tools.tools[0].name, "get_resource");

  const result = await client.callTool({
    name: "get_resource",
    arguments: { id: "abc-123" },
  });

  assert.deepEqual(result.structuredContent, payload);
  assert.equal(result.isError, undefined);

  await client.close();
});

test("REST failures remain visible as tool errors", async () => {
  const restFetch = async () =>
    new Response(JSON.stringify({ error: "not found" }), {
      status: 404,
      headers: { "content-type": "application/json" },
    });

  const handler = createMcpHandler(() =>
    buildServer({
      apiBaseUrl: "https://api.example.test",
      fetchImpl: restFetch,
    }),
  );

  const client = new Client({
    name: "integration-test-client",
    version: "0.1.0",
  });

  const transport = new StreamableHTTPClientTransport(
    new URL("http://mcp.example.test/mcp"),
    {
      fetch: (url, init) => handler.fetch(new Request(url, init)),
    },
  );

  await client.connect(transport);

  const result = await client.callTool({
    name: "get_resource",
    arguments: { id: "missing" },
  });

  assert.equal(result.isError, true);
  assert.match(result.content[0].text, /REST API error 404/);

  await client.close();
});
