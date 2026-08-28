"""
Income verification, cash flow stability, and DTI debt-to-income tools for income_employment_agent.
"""

from typing import Dict, Any


def verify_income_and_employment(
    employer_name: str,
    job_title: str,
    years_at_employer: float,
    years_in_profession: float,
    employment_type: str,
    stated_monthly_gross_income: float
) -> Dict[str, Any]:
    """
    Verifies employment continuity, stability, and validates gross monthly qualifying income (VOE / Tax transcript analysis).
    """
    stability = "HIGH_STABILITY"
    verified_income = stated_monthly_gross_income
    variance_pct = 0.0

    if employment_type in ("SELF_EMPLOYED", "1099_CONTRACTOR"):
        if years_in_profession < 2.0:
            stability = "REQUIRES_AUDIT"
            verified_income = stated_monthly_gross_income * 0.85  # Standard 15% write-off haircut
            variance_pct = -15.0
        else:
            stability = "MODERATE_STABILITY"
            verified_income = stated_monthly_gross_income * 0.95
            variance_pct = -5.0
    elif years_at_employer < 1.0 and years_in_profession < 2.0:
        stability = "REQUIRES_AUDIT"
    elif years_at_employer >= 2.0:
        stability = "HIGH_STABILITY"

    return {
        "employer_name": employer_name,
        "job_title": job_title,
        "employment_type": employment_type,
        "years_at_employer": years_at_employer,
        "years_in_profession": years_in_profession,
        "stated_monthly_gross_income": stated_monthly_gross_income,
        "verified_gross_monthly_income": round(verified_income, 2),
        "income_variance_pct": variance_pct,
        "employment_stability": stability,
        "requires_2yr_tax_transcripts": employment_type in ("SELF_EMPLOYED", "1099_CONTRACTOR")
    }


def calculate_dti_and_cashflow(
    verified_monthly_gross_income: float,
    monthly_debt_obligations: float,
    requested_loan_amount: float,
    base_interest_rate: float = 6.75,
    loan_term_months: int = 360,
    property_tax_annual_rate: float = 0.012,
    homeowners_ins_annual: float = 1800.0,
    liquid_reserves: float = 25000.0,
    loan_type: str = "CONVENTIONAL"
) -> Dict[str, Any]:
    """
    Calculates proposed PITI payment, Front-End Housing DTI, Back-End Total DTI, and Reserve Months coverage.
    """
    if verified_monthly_gross_income <= 0:
        return {
            "error": "Verified monthly income must be greater than zero.",
            "dti_compliant": False
        }

    # Monthly Principal & Interest Calculation: M = P * [r(1+r)^n] / [(1+r)^n - 1]
    monthly_rate = (base_interest_rate / 100.0) / 12.0
    num_payments = loan_term_months
    if monthly_rate > 0:
        factor = (1 + monthly_rate) ** num_payments
        monthly_pi = requested_loan_amount * (monthly_rate * factor) / (factor - 1)
    else:
        monthly_pi = requested_loan_amount / num_payments

    # Estimated Monthly Taxes and Insurance (escrow)
    estimated_property_value = requested_loan_amount / 0.80  # Baseline approximation
    monthly_taxes = (estimated_property_value * property_tax_annual_rate) / 12.0
    monthly_insurance = homeowners_ins_annual / 12.0
    proposed_monthly_housing_payment = monthly_pi + monthly_taxes + monthly_insurance

    # DTI ratios
    front_end_dti = (proposed_monthly_housing_payment / verified_monthly_gross_income) * 100.0
    total_monthly_obligations = proposed_monthly_housing_payment + monthly_debt_obligations
    back_end_dti = (total_monthly_obligations / verified_monthly_gross_income) * 100.0

    # Benchmark limits
    if loan_type == "FHA":
        dti_ceiling = 46.9
        front_ceiling = 31.0
    elif loan_type == "JUMBO":
        dti_ceiling = 43.0
        front_ceiling = 28.0
    else:  # Conventional Fannie/Freddie
        dti_ceiling = 45.0
        front_ceiling = 28.0

    dti_compliant = back_end_dti <= dti_ceiling
    reserve_months = liquid_reserves / proposed_monthly_housing_payment if proposed_monthly_housing_payment > 0 else 0.0

    return {
        "verified_gross_monthly_income": verified_monthly_gross_income,
        "monthly_principal_interest": round(monthly_pi, 2),
        "monthly_escrow_taxes_insurance": round(monthly_taxes + monthly_insurance, 2),
        "proposed_monthly_housing_payment": round(proposed_monthly_housing_payment, 2),
        "total_monthly_obligations": round(total_monthly_obligations, 2),
        "front_end_dti_pct": round(front_end_dti, 2),
        "back_end_dti_pct": round(back_end_dti, 2),
        "dti_guideline_max": dti_ceiling,
        "front_end_guideline_max": front_ceiling,
        "dti_compliant": dti_compliant,
        "liquid_reserves": liquid_reserves,
        "reserves_months": round(reserve_months, 2),
        "reserves_compliant": reserve_months >= 2.0
    }
