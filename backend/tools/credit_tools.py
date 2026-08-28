"""
Credit bureau, tradeline analysis, and risk scoring tools for credit_analyst_agent.
"""

from typing import Dict, Any, List


def fetch_credit_report(
    borrower_id: str,
    ssn_last4: str,
    credit_score: int,
    delinquencies_last_24m: int = 0,
    bankruptcy_flag: bool = False,
    prior_foreclosure_flag: bool = False
) -> Dict[str, Any]:
    """
    Simulates tri-merge credit bureau pull (Equifax, Experian, TransUnion) and returns credit profile analysis.
    """
    if credit_score >= 740:
        risk_tier = "PRIME_PLUS"
        utilization = 14.5
        derogatory_summary = "Clean credit profile with pristine payment history."
        credit_approved = True
        key_factors = ["Exceptional payment history (100% on-time)", "Low revolving credit utilization (< 15%)", "Established credit depth (> 10 years)"]
    elif credit_score >= 680:
        risk_tier = "PRIME"
        utilization = 28.2
        derogatory_summary = "Solid credit profile meeting standard agency prime guidelines."
        credit_approved = True
        key_factors = ["Good payment history", "Moderate revolving balance utilization", "Multiple seasoned tradelines"]
    elif credit_score >= 620:
        risk_tier = "NEAR_PRIME"
        utilization = 48.0
        derogatory_summary = "Acceptable credit with minor late payments in revolving accounts."
        credit_approved = not (bankruptcy_flag or prior_foreclosure_flag or delinquencies_last_24m > 2)
        key_factors = ["Elevated revolving utilization", f"{delinquencies_last_24m} minor late marks recorded", "Eligible for FHA or pricing-adjusted conventional"]
    else:
        risk_tier = "SUBPRIME"
        utilization = 75.0
        derogatory_summary = "High credit risk with serious derogatory events and elevated debt burden."
        credit_approved = False
        key_factors = ["FICO below minimum agency threshold (620)", "High delinquency concentration", "Subprime risk profile"]

    if bankruptcy_flag or prior_foreclosure_flag:
        credit_approved = False
        derogatory_summary += " Severe public record flag: active bankruptcy/foreclosure seasoning period unsatisfied."

    return {
        "borrower_id": borrower_id,
        "ssn_last4": ssn_last4,
        "fico_score": credit_score,
        "risk_grade": risk_tier,
        "revolving_utilization_pct": utilization,
        "derogatory_summary": derogatory_summary,
        "delinquencies_count": delinquencies_last_24m,
        "public_records": {
            "bankruptcy": bankruptcy_flag,
            "foreclosure": prior_foreclosure_flag
        },
        "key_factors": key_factors,
        "credit_approved": credit_approved
    }


def analyze_debt_obligations(
    monthly_debt_obligations: float,
    credit_score: int,
    revolving_utilization_pct: float = 25.0
) -> Dict[str, Any]:
    """
    Evaluates current monthly non-housing debt obligations and revolving leverage capacity.
    """
    leverage_risk = "LOW"
    if monthly_debt_obligations > 2500 or revolving_utilization_pct > 50:
        leverage_risk = "HIGH"
    elif monthly_debt_obligations > 1200 or revolving_utilization_pct > 30:
        leverage_risk = "MODERATE"

    return {
        "monthly_debt_obligations": monthly_debt_obligations,
        "revolving_utilization_pct": revolving_utilization_pct,
        "leverage_risk_level": leverage_risk,
        "debt_service_stability": "STABLE" if leverage_risk != "HIGH" else "VOLATILE"
    }
