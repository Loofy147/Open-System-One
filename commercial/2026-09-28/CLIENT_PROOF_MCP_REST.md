# Client Proof — MCP → REST Integration

## One-screen summary

**Problem matched:** build a lightweight MCP server that exposes a third-party REST API to Claude with key-based authentication, structured JSON, and a working test.

**What exists now:** a narrow Node.js proof artifact in this repository.

### Verified design surface

```
MCP client
   ↓
Streamable HTTP
   ↓
typed MCP tool
   ↓
validated input
   ↓
REST GET
   ↓
Bearer key
   ↓
JSON result / explicit error
```

### Relevant files

- [Server implementation](../../tree/research/self-conversion-primitive-v0/examples/mcp-rest-bridge/src/server.js)
- [HTTP entry](../../blob/research/self-conversion-primitive-v0/examples/mcp-rest-bridge/src/http.js)
- [stdio entry](../../blob/research/self-conversion-primitive-v0/examples/mcp-rest-bridge/src/stdio.js)
- [Integration test](../../blob/research/self-conversion-primitive-v0/examples/mcp-rest-bridge/test/integration.test.js)
- [README / scope](../../blob/research/self-conversion-primitive-v0/examples/mcp-rest-bridge/README.md)

### What is deliberately not claimed

This is a portfolio proof, not a customer deployment. It does not claim prior production delivery for a named client, and the test uses a deterministic in-process REST mock.

### Exact screening answer

A REST API exposes resources through standard HTTP requests such as GET and POST and typically returns structured representations such as JSON. With key-based authentication, the client sends the provider-issued secret in the provider's documented request header (commonly an Authorization header), and the API validates that key before serving the protected request.

### Preferred implementation

**Node.js.** It gives a small server footprint and maps cleanly to the current MCP TypeScript SDK v2 HTTP and stdio server entries.

### Delivery pattern

1. Map the supplied API brief into typed MCP tools.
2. Implement authentication at the server boundary.
3. Map each required REST endpoint to structured MCP output.
4. Add deterministic success and failure tests.
5. Configure the requested lightweight host.
6. Deliver source, setup instructions, test evidence and a concise handoff.

**Commercial positioning:** fixed-scope Phase 1, narrow surface first, no unnecessary database/frontend layer.
