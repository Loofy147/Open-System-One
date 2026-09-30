from __future__ import annotations

from dataclasses import dataclass


ACTIONS_REQUIRING_APPROVAL = frozenset(
    {
        "external_publish",
        "send_message",
        "send_email",
        "merge_code",
        "delete_data",
        "purchase",
        "financial_commitment",
        "schedule_change",
        "production_change",
        "credential_change",
        "permission_change",
    }
)


@dataclass(frozen=True)
class ActionEvaluation:
    category: str
    target: str | None
    requires_approval: bool
    authorized: bool
    reason: str


def evaluate_action(
    *,
    category: str,
    target: str | None = None,
    explicit_authorization: bool = False,
    disposable_environment: bool = False,
) -> ActionEvaluation:
    """Evaluate our task-contract policy, not OpenAI's internal policy."""
    requires = category in ACTIONS_REQUIRING_APPROVAL

    if category == "delete_data":
        return ActionEvaluation(
            category=category,
            target=target,
            requires_approval=True,
            authorized=explicit_authorization and disposable_environment,
            reason="destructive actions require explicit authorization and a disposable target",
        )

    if requires:
        return ActionEvaluation(
            category=category,
            target=target,
            requires_approval=True,
            authorized=explicit_authorization,
            reason="external side effects require explicit authorization",
        )

    return ActionEvaluation(
        category=category,
        target=target,
        requires_approval=False,
        authorized=True,
        reason="read-only or locally contained action under this contract",
    )
