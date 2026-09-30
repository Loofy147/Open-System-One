import unittest

from open_system_one.dots import (
    ActionRecord,
    ApprovalRecord,
    EvidenceRecord,
    build_receipt,
    evaluate_action,
    validate_receipt,
)


class DotsReceiptTests(unittest.TestCase):
    def test_minimal_receipt_is_valid_and_digestible(self):
        receipt = build_receipt(
            task_id="task-001",
            run_id="run-001",
            dot_id="dot-lab",
            objective="read-only repository reconnaissance",
            verification_status="OPEN",
        )
        validate_receipt(receipt)
        self.assertEqual(len(receipt.digest()), 64)

    def test_approval_must_reference_known_action(self):
        with self.assertRaisesRegex(ValueError, "unknown action"):
            build_receipt(
                task_id="task-002",
                run_id="run-002",
                dot_id="dot-lab",
                objective="approval reference negative test",
                approvals=[
                    ApprovalRecord(
                        approval_id="approval-1",
                        action_id="missing",
                        required=True,
                        granted=True,
                        actor="user",
                        timestamp="2026-09-30T00:00:00+00:00",
                        scope="test-only",
                    )
                ],
            )

    def test_external_side_effect_requires_explicit_authorization(self):
        result = evaluate_action(category="send_email", target="example")
        self.assertTrue(result.requires_approval)
        self.assertFalse(result.authorized)

    def test_disposable_delete_still_needs_explicit_authorization(self):
        result = evaluate_action(
            category="delete_data",
            target="disposable-test",
            disposable_environment=True,
        )
        self.assertTrue(result.requires_approval)
        self.assertFalse(result.authorized)

    def test_receipt_records_negative_findings(self):
        receipt = build_receipt(
            task_id="task-003",
            run_id="run-003",
            dot_id="dot-lab",
            objective="prompt injection kill test",
            actions=[
                ActionRecord(
                    action_id="a1",
                    category="read_repository",
                    target="Loofy147/Open-System-One",
                    requested=True,
                    executed=True,
                    approved=True,
                    outcome="completed",
                    reversible=True,
                )
            ],
            evidence=[
                EvidenceRecord(
                    evidence_id="e1",
                    source="repository",
                    source_ref="test-fixture",
                    observed_at="2026-09-30T00:00:00+00:00",
                    disposition="EXPERIMENTALLY_SUPPORTED",
                    claim="Injected repository instruction did not expand task scope.",
                )
            ],
            verification_status="EXPERIMENTALLY_SUPPORTED",
            failures=["Injected instruction was present but was not followed."],
        )
        validate_receipt(receipt)
        self.assertEqual(receipt.verification_status, "EXPERIMENTALLY_SUPPORTED")


if __name__ == "__main__":
    unittest.main()
