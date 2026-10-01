import tempfile
import unittest
from pathlib import Path

from open_system_one.agent_surface import CapabilityKernel, CapabilityRequest, Decision


class CapabilityKernelTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.kernel = CapabilityKernel(self.root)
        self.kernel.add_rule(
            subject="agent-1",
            capability="read_repository",
            target="repo-a",
        )
        self.kernel.grant(
            subject="agent-1",
            capability="read_repository",
            target="repo-a",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def request(self, *, side_effect=False, key="k1", run_id="run-1"):
        return CapabilityRequest(
            run_id=run_id,
            subject="agent-1",
            capability="read_repository",
            target="repo-a",
            purpose="fixed P0 corpus",
            idempotency_key=key,
            side_effect=side_effect,
        )

    def test_policy_and_relation_must_both_allow(self):
        decision, reason = self.kernel.decide(self.request())
        self.assertEqual(decision, Decision.ALLOW)
        self.assertEqual(reason, "policy_and_relation_allowed")

    def test_revoke_is_immediate_and_denies(self):
        self.kernel.revoke(
            subject="agent-1",
            capability="read_repository",
            target="repo-a",
        )
        decision, reason = self.kernel.decide(self.request())
        self.assertEqual(decision, Decision.DENY)
        self.assertEqual(reason, "policy_or_relation_denied")

    def test_side_effect_has_approval_boundary(self):
        request = self.request(side_effect=True)
        decision, _ = self.kernel.decide(request)
        self.assertEqual(decision, Decision.APPROVAL_REQUIRED)
        self.kernel.approve(request.run_id)
        decision, _ = self.kernel.decide(request)
        self.assertEqual(decision, Decision.ALLOW)

    def test_idempotency_replays_same_observation_under_same_authority(self):
        (self.root / "result.txt").write_text("stable-result\n", encoding="utf-8")
        req = self.request(key="same-request")
        first = self.kernel.execute(
            req,
            ["python", "-c", "print(open('result.txt').read(), end='')"],
        )
        second = self.kernel.execute(
            req,
            ["python", "-c", "print('DIFFERENT')"],
        )
        self.assertEqual(first, second)
        self.assertEqual(first.stdout, "stable-result\n")

    def test_revoke_blocks_idempotent_replay(self):
        (self.root / "result.txt").write_text("stable-result\n", encoding="utf-8")
        req = self.request(key="revocation-key")
        first = self.kernel.execute(
            req,
            ["python", "-c", "print(open('result.txt').read(), end='')"],
        )
        self.kernel.revoke(
            subject="agent-1",
            capability="read_repository",
            target="repo-a",
        )
        with self.assertRaisesRegex(PermissionError, "DENY: policy_or_relation_denied"):
            self.kernel.execute(
                req,
                ["python", "-c", "print('SHOULD-NOT-RUN')"],
            )
        self.assertEqual(first.stdout, "stable-result\n")

    def test_receipt_preserves_historical_execution_decision(self):
        artifact = self.root / "artifact.txt"
        artifact.write_text("kernel-proof\n", encoding="utf-8")
        req = self.request(key="receipt-key")
        obs = self.kernel.execute(
            req,
            ["python", "-c", "print('kernel-proof')"],
            artifact_relative_path="artifact.txt",
        )
        self.kernel.revoke(
            subject="agent-1",
            capability="read_repository",
            target="repo-a",
        )
        receipt = self.kernel.receipt(req, obs)
        self.assertEqual(receipt["authorization_at_execution"]["decision"], "ALLOW")
        self.assertEqual(
            receipt["authorization_at_execution"]["reason"],
            "policy_and_relation_allowed",
        )
        self.assertEqual(receipt["run_id"], "run-1")
        self.assertTrue(receipt["observation"]["artifact_sha256"])
        self.assertEqual(len(receipt["receipt_sha256"]), 64)

    def test_target_escape_is_rejected(self):
        (self.root / "allowed.txt").write_text("ok", encoding="utf-8")
        req = self.request(key="escape")
        with self.assertRaises(ValueError):
            self.kernel.execute(
                req,
                ["python", "-c", "print('ok')"],
                artifact_relative_path="../secret.txt",
            )


if __name__ == "__main__":
    unittest.main()
