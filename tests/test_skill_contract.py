from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_expected_contract_budget_fits_total_cap(self):
        contract = json.loads((ROOT / "tests/expected-contract.json").read_text())
        budget = contract["deep_research_budget"]
        total = (
            budget["max_default_researchers"]
            + budget["verifiers"]
            + budget["reviewers"]
            + budget["retry_reserve"]
        )
        self.assertLessEqual(total, contract["max_total_workers"])

    def test_skill_declares_upstream_mode_and_project_binding(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## 上游 Skill 模式", skill)
        self.assertIn("任何声明工作区输出路径的任务都使用匹配 project local", skill)
        self.assertIn("reserved slots", skill)

    def test_adapter_preserves_deep_research_stage_order(self):
        adapter = (ROOT / "references/upstream-skill-adapter.md").read_text(encoding="utf-8")
        verifier_position = adapter.index("verifier：1 个")
        reviewer_position = adapter.index("reviewer：1 个")
        self.assertLess(verifier_position, reviewer_position)
        self.assertIn("cited 存在并通过检查后创建", adapter)

    def test_projectless_is_limited_to_chat_only_outputs(self):
        lifecycle = (ROOT / "references/thread-lifecycle.md").read_text(encoding="utf-8")
        self.assertIn("只有纯聊天交付才能 projectless", lifecycle)

    def test_thread_routes_are_recorded_at_creation_time(self):
        contract = json.loads((ROOT / "tests/expected-contract.json").read_text())
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        adapter = (ROOT / "references/upstream-skill-adapter.md").read_text(encoding="utf-8")
        for field in contract["required_thread_audit_fields"]:
            self.assertTrue(field in skill or field in adapter, field)
        self.assertIn("每次 `create_thread` 成功后", adapter)
        self.assertIn("禁止依赖事后反查", adapter)


if __name__ == "__main__":
    unittest.main()
