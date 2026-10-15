import { createMcpHandler } from "@modelcontextprotocol/server";
import { buildServer } from "./server.js";

const apiBaseUrl = process.env.API_BASE_URL;
const apiKey = process.env.API_KEY;

export const handler = createMcpHandler(() =>
  buildServer({
    apiBaseUrl,
    apiKey,
    fetchImpl: globalThis.fetch,
  }),
);

export default handler;
