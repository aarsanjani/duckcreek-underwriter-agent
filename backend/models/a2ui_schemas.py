"""
A2UI Schema Models and Dynamic Component Factory for Loan Underwriting.
Conforms to the dynamic schema delivery specifications defined in architecture.md.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class A2UIBaseComponent(BaseModel):
    id: str
    type: str
    title: Optional[str] = None
    custom_classes: Optional[str] = None


class MetricBadge(BaseModel):
    label: str
    value: str
    status: str = "neutral"  # success, warning, danger, info, neutral
    subtext: Optional[str] = None


class TableComponent(A2UIBaseComponent):
    type: str = "Table"
    headers: List[str]
    rows: List[List[Any]]
    highlight_rows: Optional[List[int]] = None


class CardComponent(A2UIBaseComponent):
    type: str = "Card"
    subtitle: Optional[str] = None
    content: Optional[str] = None
    badges: Optional[List[MetricBadge]] = None
    key_value_pairs: Optional[Dict[str, str]] = None
    status_tag: Optional[str] = None


class ConditionListComponent(A2UIBaseComponent):
    type: str = "ConditionList"
    conditions: List[Dict[str, Any]]


class RiskGaugeComponent(A2UIBaseComponent):
    type: str = "RiskGauge"
    score: float
    max_score: float = 100.0
    risk_level: str
    explanation: str


class TabsComponent(A2UIBaseComponent):
    type: str = "Tabs"
    components: List[Dict[str, Any]]


class A2UIPayload(BaseModel):
    author: str = "LeadUnderwritingOrchestrator"
    ui_specification: str = "0.9"
    payload: Dict[str, Any]


def build_loan_header_a2ui(application_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Generates the Loan Header Summary Card in A2UI format."""
    borrower = application_dict.get("borrower", {})
    loan = application_dict.get("loan", {})
    collateral = application_dict.get("collateral", {})

    return {
        "type": "Card",
        "id": "loan_header_summary",
        "title": f"Loan Application #{loan.get('loan_id', 'APP-2026-X')}",
        "subtitle": f"{borrower.get('full_name', 'Applicant')} | {loan.get('loan_type', 'CONVENTIONAL')} ({loan.get('purpose', 'PURCHASE')})",
        "status_tag": "UNDERWRITING_IN_PROGRESS",
        "badges": [
            {
                "label": "Loan Amount",
                "value": f"${loan.get('requested_loan_amount', 0):,.0f}",
                "status": "info",
                "subtext": f"{loan.get('loan_term_months', 360)}m @ {loan.get('base_interest_rate', 6.75)}%"
            },
            {
                "label": "FICO Score",
                "value": str(borrower.get("credit_score", "N/A")),
                "status": "success" if borrower.get("credit_score", 0) >= 720 else ("warning" if borrower.get("credit_score", 0) >= 660 else "danger"),
                "subtext": f"Employer: {borrower.get('employer_name', 'N/A')}"
            },
            {
                "label": "Collateral Value",
                "value": f"${collateral.get('appraised_value', 0):,.0f}",
                "status": "info",
                "subtext": collateral.get("property_address", "Primary Residence")
            },
            {
                "label": "Liquid Reserves",
                "value": f"${borrower.get('liquid_reserves', 0):,.0f}",
                "status": "success" if borrower.get("liquid_reserves", 0) >= 20000 else "warning",
                "subtext": f"Verified Income: ${borrower.get('stated_monthly_gross_income', 0):,.0f}/mo"
            }
        ]
    }


def build_full_underwriting_tabs_a2ui(decision_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Builds the multi-tab interactive Underwriting Dossier A2UI component.
    """
    credit = decision_dict.get("credit_analysis", {})
    income = decision_dict.get("income_analysis", {})
    collateral = decision_dict.get("collateral_analysis", {})
    compliance = decision_dict.get("compliance_analysis", {})
    decision = decision_dict.get("decision", "APPROVED_WITH_CONDITIONS")
    stipulations = decision_dict.get("stipulations", [])

    # Decision color tag
    decision_status_map = {
        "APPROVED": "success",
        "APPROVED_WITH_CONDITIONS": "info",
        "SUSPENDED_PENDING_INFO": "warning",
        "DECLINED": "danger"
    }
    decision_tag = decision_status_map.get(decision, "info")

    return {
        "type": "Tabs",
        "id": "underwriting_dossier_tabs",
        "title": "Comprehensive Underwriting Decision & Analysis Dossier",
        "components": [
            {
                "title": "Executive Decision & Pricing",
                "type": "Card",
                "id": "tab_decision",
                "subtitle": f"Final Risk Tier: {credit.get('risk_grade', 'PRIME')}",
                "status_tag": decision,
                "badges": [
                    {"label": "Final Decision", "value": decision.replace('_', ' '), "status": decision_tag},
                    {"label": "Final Rate", "value": f"{decision_dict.get('recommended_interest_rate', 6.875):.3f}%", "status": "info"},
                    {"label": "LLPA Pricing Adj", "value": f"{decision_dict.get('pricing_adjustments_bps', 0):+d} bps", "status": "neutral"},
                    {"label": "Open Conditions", "value": f"{len(stipulations)} items", "status": "warning" if stipulations else "success"}
                ],
                "content": decision_dict.get("decision_summary", "Comprehensive multi-agent underwriting completed."),
                "key_value_pairs": {
                    "Credit Assessment": f"{credit.get('risk_grade', 'N/A')} (FICO {credit.get('fico_score', 'N/A')})",
                    "Back-End DTI": f"{income.get('back_end_dti_pct', 0):.1f}% (Max: {income.get('dti_guideline_max', 45.0)}%)",
                    "Loan-to-Value (LTV)": f"{collateral.get('ltv_pct', 0):.1f}% (Max: {collateral.get('ltv_guideline_max', 80.0)}%)",
                    "KYC / Fraud Clearance": "CLEARED - Low Risk" if compliance.get("compliance_approved") else "REVIEW REQUIRED"
                }
            },
            {
                "title": "The 4-C Financial Metrics Matrix",
                "type": "Table",
                "id": "tab_metrics_matrix",
                "headers": ["Underwriting Pillar", "Applicant Value", "Guideline Limit", "Assessment", "Variance / Margin"],
                "rows": [
                    [
                        "Credit History (FICO)",
                        str(credit.get("fico_score", "N/A")),
                        "≥ 680 (Prime)",
                        "COMPLIANT" if credit.get("credit_approved") else "BELOW TARGET",
                        f"{credit.get('fico_score', 0) - 680:+d} pts"
                    ],
                    [
                        "Capacity: Front-End DTI",
                        f"{income.get('front_end_dti_pct', 0):.1f}%",
                        "≤ 28.0% standard",
                        "COMPLIANT" if income.get("front_end_dti_pct", 0) <= 28.0 else "ELEVATED",
                        f"{28.0 - income.get('front_end_dti_pct', 0):+.1f}% margin"
                    ],
                    [
                        "Capacity: Back-End DTI",
                        f"{income.get('back_end_dti_pct', 0):.1f}%",
                        f"≤ {income.get('dti_guideline_max', 45.0):.1f}% ceiling",
                        "COMPLIANT" if income.get("dti_compliant") else "EXCEEDS CEILING",
                        f"{income.get('dti_guideline_max', 45.0) - income.get('back_end_dti_pct', 0):+.1f}% cushion"
                    ],
                    [
                        "Collateral: LTV Ratio",
                        f"{collateral.get('ltv_pct', 0):.1f}%",
                        f"≤ {collateral.get('ltv_guideline_max', 80.0):.1f}% threshold",
                        "COMPLIANT" if collateral.get("ltv_compliant") else "HIGH LTV",
                        f"{collateral.get('ltv_guideline_max', 80.0) - collateral.get('ltv_pct', 0):+.1f}% equity"
                    ],
                    [
                        "Compliance & Fraud Risk",
                        f"Score: {compliance.get('fraud_risk_score', 0)}/100",
                        "Score ≤ 25 (Low Risk)",
                        "CLEARED" if compliance.get("compliance_approved") else "FLAGGED",
                        "OFAC/Identity Verified"
                    ]
                ]
            },
            {
                "title": "Subagent Dossiers",
                "type": "Card",
                "id": "tab_subagent_dossiers",
                "content": "Specialist worker subagents executed isolated deep-dives across credit, income, appraisal, and KYC/AML compliance boundaries.",
                "key_value_pairs": {
                    "Credit Analyst Subagent": f"Score {credit.get('fico_score', 'N/A')} ({credit.get('risk_grade', 'N/A')}). Revolving Utilization: {credit.get('revolving_utilization_pct', 0):.1f}%. {credit.get('derogatory_summary', '')}",
                    "Income & Capacity Subagent": f"Verified Monthly Income: ${income.get('verified_gross_monthly_income', 0):,.0f}. Front DTI: {income.get('front_end_dti_pct', 0):.1f}%, Back DTI: {income.get('back_end_dti_pct', 0):.1f}%. Reserves: {income.get('reserves_months', 0):.1f} months ({income.get('employment_stability', 'N/A')}).",
                    "Collateral Valuation Subagent": f"Appraised Value: ${collateral.get('appraised_value', 0):,.0f}. LTV: {collateral.get('ltv_pct', 0):.1f}%. Condition Rating: {collateral.get('property_condition', 'N/A')}. Market Trend: {collateral.get('market_trend', 'STABLE')}.",
                    "Compliance & Fraud Subagent": f"OFAC Cleared: {compliance.get('ofac_sanctions_cleared', True)}. Identity Verified: {compliance.get('identity_verified', True)}. Synthetic ID Risk: {compliance.get('synthetic_id_risk', 'LOW')}."
                }
            },
            {
                "title": "Loan Conditions & Stipulations",
                "type": "ConditionList",
                "id": "tab_stipulations",
                "conditions": stipulations
            },
            {
                "title": "Macro / Meso / Micro Risk Evaluation",
                "type": "Card",
                "id": "tab_fcot_synthesis",
                "subtitle": "Fractal Chain of Thought (FCoT) Multi-Scale Risk Decomposition",
                "key_value_pairs": {
                    "Macro Perspective (Systemic)": decision_dict.get("macro_perspective", "Benchmark interest rate stability and systemic capital liquidity."),
                    "Meso Perspective (Cluster / Market)": decision_dict.get("meso_perspective", "Regional housing market absorption rate and localized employment cluster."),
                    "Micro Perspective (Deterministic)": decision_dict.get("micro_perspective", "Applicant specific line-item debt obligations and appraisal line items."),
                    "Defensive Action Track": " | ".join(decision_dict.get("defensive_mitigations", ["Collect verified paystubs", "Order final title policy"])),
                    "Positional Strategy Track": " | ".join(decision_dict.get("positional_recommendations", ["Lock 45-day rate commitment", "Establish escrow cushion"])),
                    "Scope-Audit Alignment": decision_dict.get("scope_audit_note", "No unexamined live risk branches detected.")
                }
            }
        ]
    }
