"""
Pydantic domain models for Loan Applications and Underwriting Evaluations.
"""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class BorrowerProfile(BaseModel):
    borrower_id: str
    full_name: str
    ssn_last4: str
    dob: str
    current_address: str
    employment_type: Literal["W2_EMPLOYED", "SELF_EMPLOYED", "1099_CONTRACTOR", "RETIRED"] = "W2_EMPLOYED"
    employer_name: str
    job_title: str
    years_at_employer: float = Field(ge=0)
    years_in_profession: float = Field(ge=0)
    stated_monthly_gross_income: float = Field(ge=0)
    verified_monthly_gross_income: Optional[float] = None
    monthly_debt_obligations: float = Field(ge=0)
    liquid_reserves: float = Field(ge=0)
    credit_score: int = Field(ge=300, le=850)
    bankruptcy_flag: bool = False
    prior_foreclosure_flag: bool = False
    delinquencies_last_24m: int = 0
    citizenship_status: Literal["US_CITIZEN", "PERMANENT_RESIDENT", "NON_PERMANENT_RESIDENT", "FOREIGN_NATIONAL"] = "US_CITIZEN"


class CollateralProfile(BaseModel):
    property_id: str
    property_address: str
    property_type: Literal["SINGLE_FAMILY", "CONDOMINIUM", "MULTI_FAMILY_2_4", "COMMERCIAL_RE"] = "SINGLE_FAMILY"
    occupancy: Literal["PRIMARY_RESIDENCE", "SECOND_HOME", "INVESTMENT"] = "PRIMARY_RESIDENCE"
    purchase_price: float = Field(ge=0)
    appraised_value: float = Field(ge=0)
    automated_valuation_confidence: float = Field(ge=0.0, le=1.0, default=0.95)
    property_condition_rating: Literal["C1", "C2", "C3", "C4", "C5", "C6"] = "C2"
    flood_zone_risk: Literal["ZONE_X_LOW", "ZONE_AE_HIGH", "ZONE_A_HIGH"] = "ZONE_X_LOW"
    environmental_flag: bool = False


class LoanDetails(BaseModel):
    loan_id: str
    loan_type: Literal["CONVENTIONAL", "JUMBO", "FHA", "VA", "COMMERCIAL_SBA"] = "CONVENTIONAL"
    purpose: Literal["PURCHASE", "RATE_TERM_REFINANCE", "CASH_OUT_REFINANCE"] = "PURCHASE"
    requested_loan_amount: float = Field(ge=0)
    loan_term_months: int = 360
    base_interest_rate: float = Field(default=6.75)
    target_amortization_type: Literal["FIXED_RATE", "ARM_5_1", "ARM_7_1"] = "FIXED_RATE"


class LoanApplication(BaseModel):
    application_id: str
    submission_timestamp: str
    borrower: BorrowerProfile
    collateral: CollateralProfile
    loan: LoanDetails
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Underwriting Analysis Results Models
class CreditFinding(BaseModel):
    fico_score: int
    risk_grade: Literal["PRIME_PLUS", "PRIME", "NEAR_PRIME", "SUBPRIME"]
    revolving_utilization_pct: float
    total_monthly_obligations: float
    derogatory_summary: str
    key_factors: List[str]
    credit_approved: bool


class IncomeFinding(BaseModel):
    verified_gross_monthly_income: float
    proposed_monthly_housing_payment: float  # PITI (Principal, Interest, Taxes, Insurance)
    front_end_dti_pct: float
    back_end_dti_pct: float
    dti_guideline_max: float
    dti_compliant: bool
    reserves_months: float
    employment_stability: Literal["HIGH_STABILITY", "MODERATE_STABILITY", "REQUIRES_AUDIT"]
    income_approved: bool


class CollateralFinding(BaseModel):
    appraised_value: float
    ltv_pct: float
    cltv_pct: float
    ltv_guideline_max: float
    ltv_compliant: bool
    property_condition: str
    equity_cushion_amount: float
    market_trend: Literal["APPRECIATING", "STABLE", "DECLINING"]
    collateral_approved: bool


class ComplianceFinding(BaseModel):
    ofac_sanctions_cleared: bool
    identity_verified: bool
    synthetic_id_risk: Literal["LOW", "MEDIUM", "HIGH"]
    fraud_risk_score: int = Field(ge=0, le=100)  # Lower is safer
    aml_red_flags: List[str] = Field(default_factory=list)
    fair_lending_compliant: bool
    compliance_approved: bool


class ConditionItem(BaseModel):
    condition_id: str
    category: Literal["PRIOR_TO_DOCS", "PRIOR_TO_FUNDING", "POST_CLOSING"]
    description: str
    assigned_to: str
    satisfied: bool = False


class UnderwritingDecision(BaseModel):
    application_id: str
    decision: Literal["APPROVED", "APPROVED_WITH_CONDITIONS", "SUSPENDED_PENDING_INFO", "DECLINED"]
    decision_summary: str
    recommended_interest_rate: float
    pricing_adjustments_bps: int  # Basis points (LLPAs)
    credit_analysis: CreditFinding
    income_analysis: IncomeFinding
    collateral_analysis: CollateralFinding
    compliance_analysis: ComplianceFinding
    stipulations: List[ConditionItem]
    macro_perspective: str
    meso_perspective: str
    micro_perspective: str
    defensive_mitigations: List[str]
    positional_recommendations: List[str]
    scope_audit_note: str
