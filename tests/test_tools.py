"""
Unit tests for Underwriting Specialist Tools (Credit, Income, Collateral, Compliance).
"""

import unittest
from backend.tools.credit_tools import fetch_credit_report, analyze_debt_obligations
from backend.tools.income_tools import verify_income_and_employment, calculate_dti_and_cashflow
from backend.tools.collateral_tools import appraise_collateral_and_ltv, evaluate_market_comparables
from backend.tools.compliance_tools import run_kyc_aml_sanctions_check, detect_fraud_indicators


class TestUnderwritingTools(unittest.TestCase):
    """Verifies deterministic underwriting calculations and business rules."""

    def test_credit_report_prime(self):
        result = fetch_credit_report(
            borrower_id="BW-001",
            ssn_last4="1234",
            credit_score=760,
            delinquencies_last_24m=0,
            bankruptcy_flag=False
        )
        self.assertEqual(result["risk_grade"], "PRIME_PLUS")
        self.assertTrue(result["credit_approved"])
        self.assertLessEqual(result["revolving_utilization_pct"], 20.0)

    def test_credit_report_subprime(self):
        result = fetch_credit_report(
            borrower_id="BW-002",
            ssn_last4="5678",
            credit_score=590,
            delinquencies_last_24m=3,
            bankruptcy_flag=True
        )
        self.assertEqual(result["risk_grade"], "SUBPRIME")
        self.assertFalse(result["credit_approved"])

    def test_income_verification_w2(self):
        result = verify_income_and_employment(
            employer_name="Google",
            job_title="Software Engineer",
            years_at_employer=4.0,
            years_in_profession=8.0,
            employment_type="W2_EMPLOYED",
            stated_monthly_gross_income=15000.0
        )
        self.assertEqual(result["employment_stability"], "HIGH_STABILITY")
        self.assertEqual(result["verified_gross_monthly_income"], 15000.0)
        self.assertFalse(result["requires_2yr_tax_transcripts"])

    def test_income_verification_self_employed_haircut(self):
        result = verify_income_and_employment(
            employer_name="Self Design Studio",
            job_title="Designer",
            years_at_employer=1.0,
            years_in_profession=1.5,
            employment_type="SELF_EMPLOYED",
            stated_monthly_gross_income=10000.0
        )
        self.assertEqual(result["employment_stability"], "REQUIRES_AUDIT")
        self.assertEqual(result["verified_gross_monthly_income"], 8500.0)
        self.assertTrue(result["requires_2yr_tax_transcripts"])

    def test_dti_calculation_compliant(self):
        dti = calculate_dti_and_cashflow(
            verified_monthly_gross_income=10000.0,
            monthly_debt_obligations=500.0,
            requested_loan_amount=300000.0,
            base_interest_rate=6.5,
            loan_term_months=360,
            liquid_reserves=40000.0
        )
        self.assertTrue(dti["dti_compliant"])
        self.assertLess(dti["back_end_dti_pct"], 45.0)
        self.assertGreaterEqual(dti["reserves_months"], 2.0)

    def test_collateral_ltv_evaluation(self):
        result = appraise_collateral_and_ltv(
            property_address="123 Main St, Austin, TX",
            property_type="SINGLE_FAMILY",
            occupancy="PRIMARY_RESIDENCE",
            purchase_price=500000.0,
            appraised_value=510000.0,
            requested_loan_amount=400000.0,
            property_condition_rating="C2"
        )
        self.assertEqual(result["ltv_pct"], 80.0)
        self.assertTrue(result["ltv_compliant"])
        self.assertFalse(result["requires_private_mortgage_insurance"])
        self.assertTrue(result["collateral_approved"])

    def test_compliance_kyc_and_fraud(self):
        kyc = run_kyc_aml_sanctions_check(
            full_name="Elena Rostova",
            ssn_last4="4821",
            dob="1989-04-12",
            current_address="450 S Congress, Austin TX"
        )
        self.assertTrue(kyc["ofac_sanctions_cleared"])
        self.assertTrue(kyc["identity_verified"])

        fraud = detect_fraud_indicators(
            stated_monthly_income=12500.0,
            verified_monthly_income=12500.0,
            appraised_value=600000.0,
            purchase_price=600000.0,
            delinquencies_last_24m=0
        )
        self.assertEqual(fraud["synthetic_id_risk"], "LOW")
        self.assertTrue(fraud["compliance_approved"])


if __name__ == "__main__":
    unittest.main()
