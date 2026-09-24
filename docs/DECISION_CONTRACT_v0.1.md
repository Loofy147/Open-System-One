# Decision Contract v0.1

## Purpose

Define the smallest machine-facing contract for probabilistic typed decisions without binding the contract to a model, runtime, provider, or action system.

## Core

A request contains:

- opaque state
- one or more independent typed questions
- a finite outcome space for every question

A backend evaluates the request and returns a keyed result per question:

QuestionId -> probability distribution over outcomes -> selected outcome

The result is data. It does not execute tools.

## Question types

Choice:
A finite named outcome space. Candidate position is not semantic identity.

Score:
A finite ordered set of levels. Order is semantic.

Noul:
A binary true/false decision with explicit labels.

## Required invariants

1. Question IDs are unique stable keys.
2. Outcome spaces are finite and contain at least two outcomes.
3. Probabilities are finite, non-negative, and sum to one.
4. The model does not own execution authority.
5. Confidence is derived from the distribution; it is not truth.
6. Policy decides accept/review/abstain/act after model output.
7. Backend and runtime implementations are replaceable.
8. Independent questions are batchable.
9. Choice semantics do not depend on candidate position.
10. Score ordering remains semantic.

## Non-goals

This contract does not specify:

- encoder architecture
- training method
- calibration algorithm
- inference hardware
- provider or API
- tool execution
- Jev compatibility or reproduction

## Open questions

- Does candidate-set interaction materially improve real typed-decision workloads?
- Is label-only or train-derived candidate representation better?
- Does a learned decision head outperform embedding similarity?
- How should calibration be represented as a durable object?
