"""
Unit tests for A2UI dynamic schema builders and declarative layout structures.
"""

import unittest
from backend.models.a2ui_schemas import build_loan_header_a2ui, build_full_underwriting_tabs_a2ui
from backend.workflows.sample_data import get_sample_application


class TestA2UiSchemas(unittest.TestCase):
    """Verifies declarative A2UI component structures."""

    def test_loan_header_builder(self):
        sample_app = get_sample_application("APP-CONV-2026")
        header_a2ui = build_loan_header_a2ui(sample_app)

        self.assertEqual(header_a2ui["type"], "Card")
        self.assertEqual(header_a2ui["id"], "loan_header_summary")
        self.assertIn("Elena Rostova", header_a2ui["subtitle"])
        self.assertEqual(len(header_a2ui["badges"]), 4)

    def test_full_underwriting_tabs_builder(self):
        sample_decision = {
            "application_id": "APP-TEST-01",
            "decision": "APPROVED_WITH_CONDITIONS",
            "decision_summary": "All credit and collateral criteria met.",
            "recommended_interest_rate": 6.75,
            "pricing_adjustments_bps": 25,
            "credit_analysis": {
                "fico_score": 750,
                "risk_grade": "PRIME_PLUS",
                "revolving_utilization_pct": 15.0,
                "derogatory_summary": "Pristine history",
                "credit_approved": True
            },
            "income_analysis": {
                "verified_gross_monthly_income": 12000.0,
                "front_end_dti_pct": 24.5,
                "back_end_dti_pct": 32.0,
                "dti_guideline_max": 45.0,
                "dti_compliant": True,
                "reserves_months": 5.2,
                "employment_stability": "HIGH_STABILITY"
            },
            "collateral_analysis": {
                "appraised_value": 500000.0,
                "ltv_pct": 75.0,
                "cltv_pct": 75.0,
                "ltv_guideline_max": 80.0,
                "ltv_compliant": True,
                "property_condition": "C2",
                "market_trend": "STABLE",
                "collateral_approved": True
            },
            "compliance_analysis": {
                "ofac_sanctions_cleared": True,
                "identity_verified": True,
                "synthetic_id_risk": "LOW",
                "fraud_risk_score": 5,
                "compliance_approved": True
            },
            "stipulations": [
                {
                    "condition_id": "COND-1",
                    "category": "PRIOR_TO_DOCS",
                    "description": "Provide 30 days recent paystubs",
                    "assigned_to": "Borrower",
                    "satisfied": False
                }
            ],
            "macro_perspective": "Stable benchmark yields",
            "meso_perspective": "Strong local market",
            "micro_perspective": "High applicant equity",
            "defensive_mitigations": ["Verify employment pre-funding"],
            "positional_recommendations": ["45-day rate lock"],
            "scope_audit_note": "Scoped to primary residence purchase."
        }

        tabs = build_full_underwriting_tabs_a2ui(sample_decision)
        self.assertEqual(tabs["type"], "Tabs")
        self.assertEqual(tabs["id"], "underwriting_dossier_tabs")
        self.assertEqual(len(tabs["components"]), 5)

        tab_types = [c["type"] for c in tabs["components"]]
        self.assertIn("Card", tab_types)
        self.assertIn("Table", tab_types)
        self.assertIn("ConditionList", tab_types)


if __name__ == "__main__":
    unittest.main()
