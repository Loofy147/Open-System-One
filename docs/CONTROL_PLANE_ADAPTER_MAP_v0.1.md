# Private Control-Plane Adapter Map v0.1

Recorded: 2026-10-05

## Purpose

Record how the private Decision Provenance MCP maps to the convergence contracts without promoting MCP, AppDeploy, or the service implementation into canonical semantic authority.

## Adapter snapshot

- App: Decision Provenance MCP
- AppDeploy snapshot: 1791164144719
- Service version: 0.3.0-private-control-plane
- Deployment state at recording: ready
- Authentication: bearer secret
- Canonical semantic authority: none; this service is an adapter/control interface

## Mapped services

| Control-plane service | Current implementation | Contract boundary |
|---|---|---|
| Runtime | start_run / get_run / set_run_state | Run identity and lifecycle |
| Provenance | decision / feedback / failure events | Decision provenance |
| Evidence | record_observation / record_verification / record_evidence_ref | Observation -> Verification -> Evidence linkage |
| Continuity | set_frontier / get_frontier | Revisioned continuation projection |
| Authority | register_authority / get_authority / list_authorities | Semantic-authority registry |
| Performance | get_run_head / append_events / inspect_run | Bounded operational access |
| Recovery | enqueue / list / claim / finish | Recovery lifecycle |
| Diagnostics | analyze / integrity / anomalies | Inspection and assurance |

## Explicit non-claims

This adapter does **not** establish:

- cross-repository semantic conformance;
- canonical execution authority;
- exactly-once external effects;
- shared-writer concurrency safety;
- cryptographic authenticity of external evidence;
- truth of evidence without independent verification;
- provider/protocol ownership of the canonical domain model.

## Current evidence

The deployment has passed its current AppDeploy validation/QA gate with no reported frontend, network, or backend errors.

This proves deployment/runtime surface health only.

It does not close G-01, G-02, G-03, or G-04.

## Next discriminating action

Execute the same P0 fixtures against at least two materially different implementations, beginning with the UWS durable Run path and the Android execution/evidence path.

Acceptance is semantic agreement plus independent evidence and exact provenance, not shared code.