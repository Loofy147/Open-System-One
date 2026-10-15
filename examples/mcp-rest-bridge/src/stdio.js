import { serveStdio } from "@modelcontextprotocol/server/stdio";
import { buildServer } from "./server.js";

const apiBaseUrl = process.env.API_BASE_URL;
const apiKey = process.env.API_KEY;

serveStdio(() =>
  buildServer({
    apiBaseUrl,
    apiKey,
    fetchImpl: globalThis.fetch,
  }),
);

console.error("[mcp-rest-bridge-demo] serving over stdio");
