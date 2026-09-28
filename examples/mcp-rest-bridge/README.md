# MCP to REST Bridge Demo

A deliberately small, auditable integration artifact.

## Flow

MCP client
  -> Streamable HTTP
  -> MCP tool
  -> validated identifier
  -> REST GET with optional Bearer credential
  -> JSON decode
  -> structured MCP result

## Current SDK baseline

The demo pins:
- @modelcontextprotocol/server 2.1.0
- @modelcontextprotocol/client 2.1.0
- zod 4.6.5

The MCP TypeScript SDK v2 line implements the 2026-07-28 protocol revision. The HTTP entry is createMcpHandler and the stdio entry is serveStdio.

## Run

npm install
npm test

The integration test uses a deterministic in-process REST mock. No customer credentials or third-party systems are contacted.

For a local stdio process:

API_BASE_URL=https://your-api.example.com API_KEY=... node src/stdio.js

## Evidence boundary

The artifact demonstrates:
- MCP tool discovery
- validated input schema
- REST request construction
- Bearer credential placement
- structured success propagation
- explicit REST error propagation

It is a portfolio/proof artifact, not a production deployment. Customer-specific authorization, retries, rate limits, persistence, observability, secret management, and API-specific schemas remain deployment work.
