# Proposal — MCP REST Bridge

Target: Upwork "MCP Server Build — Third-Party API Integration for Claude AI"
Budget shown on the listing: $500-$1,000 Phase 1.

## Client-facing proposal

Hi — this is a good fit for a narrow Node.js implementation.

**Closest comparable proof:** I built a focused MCP→REST integration artifact that exposes a typed MCP tool, validates input, calls a REST endpoint with optional Bearer authentication, returns structured JSON, and preserves REST failures as explicit tool errors. The proof includes an in-process MCP client integration test covering tool discovery, request construction, auth-header placement, structured results, and a 404 path.

**Proof:**  
https://github.com/Loofy147/Open-System-One/tree/research/self-conversion-primitive-v0/examples/mcp-rest-bridge

I would implement your Phase 1 as:

- Node.js + current MCP TypeScript SDK v2
- only the REST endpoints in your brief
- key authentication kept at the server boundary
- typed/validated MCP tool inputs
- clean structured JSON responses for Claude
- explicit HTTP and malformed-response errors
- deterministic tests for success and failure cases
- lightweight deployment configuration for Railway, Render, or your chosen host
- source + setup notes + test evidence at handoff

I would keep the first version stateless and deliberately small. No frontend, database, or unrelated framework work.

**REST API / key-auth screening answer:**  
A REST API exposes resources through standard HTTP requests such as GET and POST and commonly returns structured representations such as JSON. With key-based authentication, the client sends the provider-issued secret in the provider's documented request header (often an Authorization header), and the API validates that key before serving the protected request.

**Language:** Node.js.

**Availability:** Ready to start within the requested 3-business-day window, subject to the client's NDA/brief handoff.

**Phase 1:** $750 fixed price.

One note on evidence: the linked MCP→REST project is a portfolio proof, not a disguised customer deployment. I prefer to show the exact implementation that exists rather than claim a prior client engagement that I cannot substantiate.
