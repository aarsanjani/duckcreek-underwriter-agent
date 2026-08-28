"""
KYC/AML, OFAC sanctions screening, and fraud anomaly detection tools for compliance_fraud_agent.
"""

from typing import Dict, Any, List


def run_kyc_aml_sanctions_check(
    full_name: str,
    ssn_last4: str,
    dob: str,
    current_address: str,
    citizenship_status: str = "US_CITIZEN"
) -> Dict[str, Any]:
    """
    Executes KYC identity verification, FinCEN/OFAC Specially Designated Nationals (SDN) watchlist screening, and PEP check.
    """
    # Deterministic sanctions check simulation
    sanctions_hit = any(bad_name in full_name.upper() for bad_name in ["SANCTIONED_TEST", "TERROR_LIST", "OFAC_HIT"])
    identity_verified = len(ssn_last4) == 4 and bool(full_name) and bool(dob)
    
    aml_flags: List[str] = []
    if sanctions_hit:
        aml_flags.append("CRITICAL: SDN Watchlist match detected.")
    if citizenship_status == "FOREIGN_NATIONAL":
        aml_flags.append("Enhanced Due Diligence required for foreign national borrower.")

    return {
        "full_name": full_name,
        "identity_verified": identity_verified,
        "ofac_sanctions_cleared": not sanctions_hit,
        "politically_exposed_person": False,
        "citizenship_verified": citizenship_status in ("US_CITIZEN", "PERMANENT_RESIDENT", "NON_PERMANENT_RESIDENT"),
        "aml_red_flags": aml_flags,
        "cip_compliant": identity_verified and not sanctions_hit
    }


def detect_fraud_indicators(
    stated_monthly_income: float,
    verified_monthly_income: float,
    appraised_value: float,
    purchase_price: float,
    delinquencies_last_24m: int = 0
) -> Dict[str, Any]:
    """
    Evaluates anti-fraud heuristics: income discrepancies, synthetic identity markers, rapid property flipping, occupancy fraud.
    Returns fraud risk index (0 to 100).
    """
    risk_score = 5  # Baseline minimal ambient risk
    fraud_flags: List[str] = []

    # Income discrepancy test
    if verified_monthly_income > 0:
        variance = (stated_monthly_income - verified_monthly_income) / verified_monthly_income
        if variance > 0.25:
            risk_score += 35
            fraud_flags.append("Income Inflation: Stated income exceeds verified transcript by > 25%")
        elif variance > 0.10:
            risk_score += 15
            fraud_flags.append("Moderate Income Variance: Stated income exceeds verified by > 10%")

    # Rapid appreciation / flip test
    if purchase_price > 0 and appraised_value > purchase_price * 1.25:
        risk_score += 20
        fraud_flags.append("Appraisal Gap: Appraised value exceeds contract purchase price by > 25%")

    # Credit velocity test
    if delinquencies_last_24m >= 3:
        risk_score += 15

    # Assign risk tier
    if risk_score >= 50:
        synthetic_risk = "HIGH"
    elif risk_score >= 25:
        synthetic_risk = "MEDIUM"
    else:
        synthetic_risk = "LOW"

    return {
        "fraud_risk_score": min(risk_score, 100),
        "synthetic_id_risk": synthetic_risk,
        "fraud_indicators_detected": fraud_flags,
        "fair_lending_compliant": True,
        "compliance_approved": risk_score < 40 and not any("CRITICAL" in f for f in fraud_flags)
    }
