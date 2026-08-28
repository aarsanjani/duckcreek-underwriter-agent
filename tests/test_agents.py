"""
Unit tests for ADK 2.x Agent configurations, subagent isolation rules, and Hub-and-Spoke topology.
"""

import unittest
from backend.agents.credit_agent import create_credit_agent
from backend.agents.income_agent import create_income_agent
from backend.agents.collateral_agent import create_collateral_agent
from backend.agents.compliance_agent import create_compliance_agent
from backend.agents.orchestrator import create_underwriting_orchestrator


class TestAgentConfigurations(unittest.TestCase):
    """Verifies that ADK 2.x agent definitions adhere to the isolation best practices."""

    def test_credit_agent_isolation(self):
        agent = create_credit_agent()
        self.assertEqual(agent.name, "credit_analyst_agent")
        self.assertTrue(agent.disallow_transfer_to_parent)
        self.assertTrue(agent.disallow_transfer_to_peers)
        self.assertEqual(len(agent.tools), 2)

    def test_income_agent_isolation(self):
        agent = create_income_agent()
        self.assertEqual(agent.name, "income_employment_agent")
        self.assertTrue(agent.disallow_transfer_to_parent)
        self.assertTrue(agent.disallow_transfer_to_peers)
        self.assertEqual(len(agent.tools), 2)

    def test_collateral_agent_isolation(self):
        agent = create_collateral_agent()
        self.assertEqual(agent.name, "collateral_valuation_agent")
        self.assertTrue(agent.disallow_transfer_to_parent)
        self.assertTrue(agent.disallow_transfer_to_peers)
        self.assertEqual(len(agent.tools), 2)

    def test_compliance_agent_isolation(self):
        agent = create_compliance_agent()
        self.assertEqual(agent.name, "compliance_fraud_agent")
        self.assertTrue(agent.disallow_transfer_to_parent)
        self.assertTrue(agent.disallow_transfer_to_peers)
        self.assertEqual(len(agent.tools), 2)

    def test_orchestrator_subagent_mesh(self):
        orchestrator = create_underwriting_orchestrator()
        self.assertEqual(orchestrator.name, "underwriting_orchestrator")
        self.assertEqual(len(orchestrator.sub_agents), 4)
        subagent_names = [sa.name for sa in orchestrator.sub_agents]
        self.assertIn("credit_analyst_agent", subagent_names)
        self.assertIn("income_employment_agent", subagent_names)
        self.assertIn("collateral_valuation_agent", subagent_names)
        self.assertIn("compliance_fraud_agent", subagent_names)


if __name__ == "__main__":
    unittest.main()
