"""
Collateral appraisal, LTV/CLTV risk calculation, and property assessment tools for collateral_valuation_agent.
"""

from typing import Dict, Any


def appraise_collateral_and_ltv(
    property_address: str,
    property_type: str,
    occupancy: str,
    purchase_price: float,
    appraised_value: float,
    requested_loan_amount: float,
    property_condition_rating: str = "C2",
    flood_zone_risk: str = "ZONE_X_LOW",
    loan_type: str = "CONVENTIONAL"
) -> Dict[str, Any]:
    """
    Evaluates collateral valuation, calculates Loan-to-Value (LTV), verifies equity margin, and checks property condition rating.
    """
    # Valuation basis for purchase is lesser of purchase price or appraised value
    valuation_basis = min(purchase_price, appraised_value) if purchase_price > 0 else appraised_value
    
    if valuation_basis <= 0:
        return {
            "error": "Valuation basis must be greater than zero.",
            "ltv_compliant": False
        }

    ltv_pct = (requested_loan_amount / valuation_basis) * 100.0
    cltv_pct = ltv_pct  # Assuming single lien unless subordinate financing exists
    equity_cushion_amount = valuation_basis - requested_loan_amount

    # Guideline ceilings
    if loan_type == "FHA":
        ltv_ceiling = 96.5
    elif loan_type == "VA":
        ltv_ceiling = 100.0
    elif loan_type == "JUMBO":
        ltv_ceiling = 80.0
    elif loan_type == "COMMERCIAL_SBA":
        ltv_ceiling = 85.0
    else:  # Conventional
        ltv_ceiling = 80.0 if occupancy == "INVESTMENT" else 95.0

    ltv_compliant = ltv_pct <= ltv_ceiling
    requires_pmi = ltv_pct > 80.0 and loan_type == "CONVENTIONAL"
    
    # Condition risk check (C5/C6 are sub-standard uninhabitable)
    condition_acceptable = property_condition_rating in ("C1", "C2", "C3", "C4")
    flood_insurance_required = flood_zone_risk in ("ZONE_AE_HIGH", "ZONE_A_HIGH")

    return {
        "property_address": property_address,
        "property_type": property_type,
        "occupancy": occupancy,
        "appraised_value": appraised_value,
        "purchase_price": purchase_price,
        "valuation_basis": valuation_basis,
        "requested_loan_amount": requested_loan_amount,
        "ltv_pct": round(ltv_pct, 2),
        "cltv_pct": round(cltv_pct, 2),
        "ltv_guideline_max": ltv_ceiling,
        "ltv_compliant": ltv_compliant,
        "equity_cushion_amount": round(equity_cushion_amount, 2),
        "requires_private_mortgage_insurance": requires_pmi,
        "property_condition_rating": property_condition_rating,
        "condition_acceptable": condition_acceptable,
        "flood_insurance_required": flood_insurance_required,
        "collateral_approved": ltv_compliant and condition_acceptable
    }


def evaluate_market_comparables(
    property_address: str,
    property_type: str,
    market_trend: str = "STABLE"
) -> Dict[str, Any]:
    """
    Analyzes local real estate comps, inventory absorption, and price appreciation velocity.
    """
    return {
        "property_address": property_address,
        "market_trend": market_trend,
        "neighborhood_absorption_rate_months": 2.4,
        "comparable_sales_variance_pct": 2.1,
        "liquidation_risk": "LOW" if market_trend in ("APPRECIATING", "STABLE") else "MODERATE"
    }
