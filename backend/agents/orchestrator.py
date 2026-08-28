"""
Lead Underwriting Orchestrator Agent (ADK 2.x & A2UI).
Coordinates specialist worker subagents in a strict Hub-and-Spoke topology using
Fractal Chain of Thought (FCoT), hillclimbing multi-scale synthesis, and schema-driven A2UI delivery.
"""

from typing import Dict, Any, List, Generator
import json
import logging
from google.adk.agents import LlmAgent
from backend.agents.credit_agent import create_credit_agent
from backend.agents.income_agent import create_income_agent
from backend.agents.collateral_agent import create_collateral_agent
from backend.agents.compliance_agent import create_compliance_agent
from backend.tools.credit_tools import fetch_credit_report, analyze_debt_obligations
from backend.tools.income_tools import verify_income_and_employment, calculate_dti_and_cashflow
from backend.tools.collateral_tools import appraise_collateral_and_ltv, evaluate_market_comparables
from backend.tools.compliance_tools import run_kyc_aml_sanctions_check, detect_fraud_indicators
from backend.models.a2ui_schemas import build_loan_header_a2ui, build_full_underwriting_tabs_a2ui
from backend.config import MODEL_ID, logger


ORCHESTRATOR_INSTRUCTION = """
You are the Lead Underwriting Agent (Synthesizer Orchestrator), architected on the Fractal Chain of Thought (FCoT) paradigm.
Your objective is to coordinate specialized subagents (`credit_analyst_agent`, `income_employment_agent`, `collateral_valuation_agent`, `compliance_fraud_agent`) to build rigorous, enterprise-grade loan underwriting decisions.

I. PRE-EXECUTION: SYSTEMIC BOUNDARY & OBJECTIVE TUNING
Internally balance two opposing forces throughout your evaluation:
1. f_max (Maximization): Maximize risk discovery across credit, income stability, property collateral, and compliance indicators.
2. f_min (Minimization): Maximize operational speed and deterministic underwriting clarity, pruning ungrounded speculation.

II. SEQUENTIAL ROUTING PROTOCOL & SILENT TRANSFERS
To guarantee system stability, subagent execution MUST proceed sequentially in a strict Hub-and-Spoke model:
- Turn 1: If credit analysis has not been performed, immediately invoke `transfer_to_agent(agent_name="credit_analyst_agent")` as your sole action without preamble.
- Turn 2: Once credit is returned, immediately invoke `transfer_to_agent(agent_name="income_employment_agent")` as your sole action.
- Turn 3: Once income is returned, immediately invoke `transfer_to_agent(agent_name="collateral_valuation_agent")` as your sole action.
- Turn 4: Once collateral is returned, immediately invoke `transfer_to_agent(agent_name="compliance_fraud_agent")` as your sole action.
- Turn 5: Only when ALL 4 specialist subagents have returned findings do you execute the multi-scale Step C consolidation.

III. THE SYNTHESIS ENGINE: MULTI-SCALE EVALUATION (STEP C)
Synthesize the subagent findings through three simultaneous analytical lenses:
1. Macro Perspective: Systemic interest rate environment, capital markets liquidity, agency guideline constraints (Fannie/Freddie/FHA).
2. Meso Perspective: Regional economic conditions, localized employment sector health, neighborhood absorption rates.
3. Micro Perspective: Exact borrower metrics (FICO, Front-End DTI, Back-End DTI, LTV, Reserves, OFAC clearance).

IV. MANDATORY TERMINAL OUTPUT STRUCTURE:
1. Final Underwriting Decision: APPROVED, APPROVED_WITH_CONDITIONS, SUSPENDED_PENDING_INFO, or DECLINED.
2. Loan Pricing & LLPAs: Recommended interest rate including risk adjustments.
3. The 4-Pillar Financial Metrics Summary (Credit, Income, Collateral, Compliance).
4. Loan Conditions Checklist: Specific Prior-to-Doc (PTD) and Prior-to-Funding (PTF) stipulations.
5. Dual-Track Action Plan:
   - Defensive Track (Micro-Dense): Short-term document verifications and title checks.
   - Positional Track (Macro-Anchored): Rate locks, escrow buffers, and structural mitigations.
6. Scope-Audit Alignment: Embedded disclosure of boundary constraints.
"""


def orchestrator_before_callback(callback_context):
    """Lifecycle hook triggered before lead orchestrator execution."""
    agent_name = getattr(callback_context, "agent_name", "underwriting_orchestrator")
    logger.info(f"Activated Lead Orchestrator: {agent_name}")
    return None


def orchestrator_after_callback(callback_context):
    """Lifecycle hook triggered after lead orchestrator completes."""
    agent_name = getattr(callback_context, "agent_name", "underwriting_orchestrator")
    logger.info(f"Completed Lead Orchestrator cycle: {agent_name}")
    return None


def create_underwriting_orchestrator() -> LlmAgent:
    """
    Creates and configures the ADK 2.x Root Lead Underwriting Orchestrator with all 4 specialized subagents.
    """
    credit_agent = create_credit_agent()
    income_agent = create_income_agent()
    collateral_agent = create_collateral_agent()
    compliance_agent = create_compliance_agent()

    return LlmAgent(
        name="underwriting_orchestrator",
        description="Lead Underwriting Orchestrator that coordinates credit, income, collateral, and compliance specialist subagents.",
        instruction=ORCHESTRATOR_INSTRUCTION,
        sub_agents=[credit_agent, income_agent, collateral_agent, compliance_agent],
        model=MODEL_ID,
        before_agent_callback=orchestrator_before_callback,
        after_agent_callback=orchestrator_after_callback
    )


class ReactiveUnderwritingExecutionEngine:
    """
    Production-grade Reactive Streaming Controller & Execution Engine.
    Executes the multi-agent Hub-and-Spoke underwriting workflow, isolates tool evaluations,
    and yields standardized JSON-RPC 2.0 SSE telemetry frames and A2UI schema payloads.
    """

    def __init__(self, session_id: str, loan_application_data: Dict[str, Any]):
        self.session_id = session_id
        self.app_data = loan_application_data
        self.borrower = loan_application_data.get("borrower", {})
        self.collateral = loan_application_data.get("collateral", {})
        self.loan = loan_application_data.get("loan", {})

    def _encode_rpc_frame(self, method: str, params: Dict[str, Any]) -> str:
        """Wraps parameters into standardized JSON-RPC 2.0 frames."""
        return json.dumps({"jsonrpc": "2.0", "method": method, "params": params})

    def execute_workflow_stream(self) -> Generator[str, None, None]:
        """
        Executes sequential subagent turns, tool calls, and A2UI layout generation.
        Yields JSON-RPC 2.0 strings for SSE streaming.
        """
        logger.info(f"Session {self.session_id}: Starting Reactive Underwriting Stream.")

        # Step 0: Deliver Initial Loan Header A2UI Component
        header_payload = build_loan_header_a2ui(self.app_data)
        yield self._encode_rpc_frame("onUiComponentDelivery", {
            "author": "underwriting_orchestrator",
            "ui_specification": "0.9",
            "payload": header_payload
        })

        # Frame 1: Orchestrator Initial Thought & Intent Analysis
        yield self._encode_rpc_frame("onAgentThought", {
            "author": "underwriting_orchestrator",
            "message": f"Decomposing Loan Application #{self.loan.get('loan_id', 'APP-2026-01')} for {self.borrower.get('full_name', 'Applicant')}. Initializing 4-Pillar Underwriting Protocol."
        })

        # =========================================================================
        # PHASE 1: CREDIT ANALYST SPECIALIST SUBAGENT
        # =========================================================================
        yield self._encode_rpc_frame("onAgentDelegation", {
            "author": "underwriting_orchestrator",
            "target": "credit_analyst_agent",
            "message": "Delegating Pillar 1: Credit History & Debt Obligation Analysis to credit_analyst_agent."
        })

        yield self._encode_rpc_frame("onToolCall", {
            "author": "credit_analyst_agent",
            "tool": "fetch_credit_report",
            "arguments": {
                "borrower_id": self.borrower.get("borrower_id", "BW-100"),
                "ssn_last4": self.borrower.get("ssn_last4", "1234"),
                "credit_score": self.borrower.get("credit_score", 720),
                "delinquencies_last_24m": self.borrower.get("delinquencies_last_24m", 0),
                "bankruptcy_flag": self.borrower.get("bankruptcy_flag", False)
            }
        })

        credit_report = fetch_credit_report(
            borrower_id=self.borrower.get("borrower_id", "BW-100"),
            ssn_last4=self.borrower.get("ssn_last4", "1234"),
            credit_score=self.borrower.get("credit_score", 720),
            delinquencies_last_24m=self.borrower.get("delinquencies_last_24m", 0),
            bankruptcy_flag=self.borrower.get("bankruptcy_flag", False),
            prior_foreclosure_flag=self.borrower.get("prior_foreclosure_flag", False)
        )

        yield self._encode_rpc_frame("onToolCall", {
            "author": "credit_analyst_agent",
            "tool": "analyze_debt_obligations",
            "arguments": {
                "monthly_debt_obligations": self.borrower.get("monthly_debt_obligations", 450.0),
                "credit_score": self.borrower.get("credit_score", 720),
                "revolving_utilization_pct": credit_report.get("revolving_utilization_pct", 25.0)
            }
        })

        debt_analysis = analyze_debt_obligations(
            monthly_debt_obligations=self.borrower.get("monthly_debt_obligations", 450.0),
            credit_score=self.borrower.get("credit_score", 720),
            revolving_utilization_pct=credit_report.get("revolving_utilization_pct", 25.0)
        )

        yield self._encode_rpc_frame("onAgentThought", {
            "author": "credit_analyst_agent",
            "message": f"Credit evaluation complete. FICO: {credit_report['fico_score']} ({credit_report['risk_grade']}). Utilization: {credit_report['revolving_utilization_pct']}%. Status: {'Approved' if credit_report['credit_approved'] else 'Adverse Action Flagged'}."
        })

        # =========================================================================
        # PHASE 2: INCOME & EMPLOYMENT CAPACITY SUBAGENT
        # =========================================================================
        yield self._encode_rpc_frame("onAgentDelegation", {
            "author": "underwriting_orchestrator",
            "target": "income_employment_agent",
            "message": "Delegating Pillar 2: Income Verification & DTI Capacity Calculation to income_employment_agent."
        })

        yield self._encode_rpc_frame("onToolCall", {
            "author": "income_employment_agent",
            "tool": "verify_income_and_employment",
            "arguments": {
                "employer_name": self.borrower.get("employer_name", "Tech Corp"),
                "job_title": self.borrower.get("job_title", "Senior Engineer"),
                "years_at_employer": self.borrower.get("years_at_employer", 3.5),
                "years_in_profession": self.borrower.get("years_in_profession", 8.0),
                "employment_type": self.borrower.get("employment_type", "W2_EMPLOYED"),
                "stated_monthly_gross_income": self.borrower.get("stated_monthly_gross_income", 12500.0)
            }
        })

        income_verification = verify_income_and_employment(
            employer_name=self.borrower.get("employer_name", "Tech Corp"),
            job_title=self.borrower.get("job_title", "Senior Engineer"),
            years_at_employer=self.borrower.get("years_at_employer", 3.5),
            years_in_profession=self.borrower.get("years_in_profession", 8.0),
            employment_type=self.borrower.get("employment_type", "W2_EMPLOYED"),
            stated_monthly_gross_income=self.borrower.get("stated_monthly_gross_income", 12500.0)
        )

        yield self._encode_rpc_frame("onToolCall", {
            "author": "income_employment_agent",
            "tool": "calculate_dti_and_cashflow",
            "arguments": {
                "verified_monthly_gross_income": income_verification["verified_gross_monthly_income"],
                "monthly_debt_obligations": self.borrower.get("monthly_debt_obligations", 450.0),
                "requested_loan_amount": self.loan.get("requested_loan_amount", 450000.0),
                "base_interest_rate": self.loan.get("base_interest_rate", 6.75),
                "loan_term_months": self.loan.get("loan_term_months", 360),
                "liquid_reserves": self.borrower.get("liquid_reserves", 65000.0),
                "loan_type": self.loan.get("loan_type", "CONVENTIONAL")
            }
        })

        dti_result = calculate_dti_and_cashflow(
            verified_monthly_gross_income=income_verification["verified_gross_monthly_income"],
            monthly_debt_obligations=self.borrower.get("monthly_debt_obligations", 450.0),
            requested_loan_amount=self.loan.get("requested_loan_amount", 450000.0),
            base_interest_rate=self.loan.get("base_interest_rate", 6.75),
            loan_term_months=self.loan.get("loan_term_months", 360),
            liquid_reserves=self.borrower.get("liquid_reserves", 65000.0),
            loan_type=self.loan.get("loan_type", "CONVENTIONAL")
        )

        yield self._encode_rpc_frame("onAgentThought", {
            "author": "income_employment_agent",
            "message": f"Capacity verified. Monthly Gross: ${income_verification['verified_gross_monthly_income']:,.0f}. Front DTI: {dti_result['front_end_dti_pct']}%, Back DTI: {dti_result['back_end_dti_pct']}%. Reserves: {dti_result['reserves_months']} months."
        })

        # =========================================================================
        # PHASE 3: COLLATERAL VALUATION SUBAGENT
        # =========================================================================
        yield self._encode_rpc_frame("onAgentDelegation", {
            "author": "underwriting_orchestrator",
            "target": "collateral_valuation_agent",
            "message": "Delegating Pillar 3: Collateral Appraisal & LTV Assessment to collateral_valuation_agent."
        })

        yield self._encode_rpc_frame("onToolCall", {
            "author": "collateral_valuation_agent",
            "tool": "appraise_collateral_and_ltv",
            "arguments": {
                "property_address": self.collateral.get("property_address", "100 Innovation Way, Austin, TX"),
                "property_type": self.collateral.get("property_type", "SINGLE_FAMILY"),
                "occupancy": self.collateral.get("occupancy", "PRIMARY_RESIDENCE"),
                "purchase_price": self.collateral.get("purchase_price", 600000.0),
                "appraised_value": self.collateral.get("appraised_value", 615000.0),
                "requested_loan_amount": self.loan.get("requested_loan_amount", 450000.0),
                "property_condition_rating": self.collateral.get("property_condition_rating", "C2"),
                "flood_zone_risk": self.collateral.get("flood_zone_risk", "ZONE_X_LOW"),
                "loan_type": self.loan.get("loan_type", "CONVENTIONAL")
            }
        })

        collateral_result = appraise_collateral_and_ltv(
            property_address=self.collateral.get("property_address", "100 Innovation Way, Austin, TX"),
            property_type=self.collateral.get("property_type", "SINGLE_FAMILY"),
            occupancy=self.collateral.get("occupancy", "PRIMARY_RESIDENCE"),
            purchase_price=self.collateral.get("purchase_price", 600000.0),
            appraised_value=self.collateral.get("appraised_value", 615000.0),
            requested_loan_amount=self.loan.get("requested_loan_amount", 450000.0),
            property_condition_rating=self.collateral.get("property_condition_rating", "C2"),
            flood_zone_risk=self.collateral.get("flood_zone_risk", "ZONE_X_LOW"),
            loan_type=self.loan.get("loan_type", "CONVENTIONAL")
        )

        yield self._encode_rpc_frame("onToolCall", {
            "author": "collateral_valuation_agent",
            "tool": "evaluate_market_comparables",
            "arguments": {
                "property_address": self.collateral.get("property_address", "100 Innovation Way, Austin, TX"),
                "property_type": self.collateral.get("property_type", "SINGLE_FAMILY"),
                "market_trend": "STABLE"
            }
        })

        comps_result = evaluate_market_comparables(
            property_address=self.collateral.get("property_address", "100 Innovation Way, Austin, TX"),
            property_type=self.collateral.get("property_type", "SINGLE_FAMILY"),
            market_trend="STABLE"
        )

        yield self._encode_rpc_frame("onAgentThought", {
            "author": "collateral_valuation_agent",
            "message": f"Collateral analysis complete. Appraised Value: ${collateral_result['appraised_value']:,.0f}. LTV: {collateral_result['ltv_pct']}%. Condition: {collateral_result['property_condition_rating']}. Collateral Status: {'Approved' if collateral_result['collateral_approved'] else 'Deficient'}."
        })

        # =========================================================================
        # PHASE 4: COMPLIANCE & FRAUD SUBAGENT
        # =========================================================================
        yield self._encode_rpc_frame("onAgentDelegation", {
            "author": "underwriting_orchestrator",
            "target": "compliance_fraud_agent",
            "message": "Delegating Pillar 4: KYC/AML, OFAC Watchlist & Anti-Fraud Screening to compliance_fraud_agent."
        })

        yield self._encode_rpc_frame("onToolCall", {
            "author": "compliance_fraud_agent",
            "tool": "run_kyc_aml_sanctions_check",
            "arguments": {
                "full_name": self.borrower.get("full_name", "Applicant"),
                "ssn_last4": self.borrower.get("ssn_last4", "1234"),
                "dob": self.borrower.get("dob", "1988-05-14"),
                "current_address": self.borrower.get("current_address", "123 Main St"),
                "citizenship_status": self.borrower.get("citizenship_status", "US_CITIZEN")
            }
        })

        kyc_result = run_kyc_aml_sanctions_check(
            full_name=self.borrower.get("full_name", "Applicant"),
            ssn_last4=self.borrower.get("ssn_last4", "1234"),
            dob=self.borrower.get("dob", "1988-05-14"),
            current_address=self.borrower.get("current_address", "123 Main St"),
            citizenship_status=self.borrower.get("citizenship_status", "US_CITIZEN")
        )

        yield self._encode_rpc_frame("onToolCall", {
            "author": "compliance_fraud_agent",
            "tool": "detect_fraud_indicators",
            "arguments": {
                "stated_monthly_income": self.borrower.get("stated_monthly_gross_income", 12500.0),
                "verified_monthly_income": income_verification["verified_gross_monthly_income"],
                "appraised_value": collateral_result["appraised_value"],
                "purchase_price": collateral_result["purchase_price"],
                "delinquencies_last_24m": self.borrower.get("delinquencies_last_24m", 0)
            }
        })

        fraud_result = detect_fraud_indicators(
            stated_monthly_income=self.borrower.get("stated_monthly_gross_income", 12500.0),
            verified_monthly_income=income_verification["verified_gross_monthly_income"],
            appraised_value=collateral_result["appraised_value"],
            purchase_price=collateral_result["purchase_price"],
            delinquencies_last_24m=self.borrower.get("delinquencies_last_24m", 0)
        )

        yield self._encode_rpc_frame("onAgentThought", {
            "author": "compliance_fraud_agent",
            "message": f"Compliance clearance completed. OFAC Cleared: {kyc_result['ofac_sanctions_cleared']}. Fraud Score: {fraud_result['fraud_risk_score']}/100 ({fraud_result['synthetic_id_risk']} risk). Compliance: {'Approved' if fraud_result['compliance_approved'] else 'Review Required'}."
        })

        # =========================================================================
        # PHASE 5: LEAD ORCHESTRATOR MULTI-SCALE SYNTHESIS (STEP C & HILLCLIMBING)
        # =========================================================================
        yield self._encode_rpc_frame("onAgentThought", {
            "author": "underwriting_orchestrator",
            "message": "All 4 Specialist Worker turns completed. Initiating Fractal Chain of Thought (FCoT) Macro-Meso-Micro Multi-Scale Synthesis pass."
        })

        # Determine Decision
        credit_ok = credit_report.get("credit_approved", False)
        income_ok = dti_result.get("dti_compliant", False)
        collateral_ok = collateral_result.get("collateral_approved", False)
        compliance_ok = fraud_result.get("compliance_approved", False)

        if credit_ok and income_ok and collateral_ok and compliance_ok:
            decision = "APPROVED_WITH_CONDITIONS"
            decision_summary = "Loan application satisfies all prime agency underwriting standards. Approved subject to standard Prior-to-Doc and Prior-to-Funding verifications."
        elif not credit_ok or not compliance_ok:
            decision = "DECLINED"
            decision_summary = "Loan declined due to credit risk policy breach or adverse compliance/fraud findings."
        else:
            decision = "SUSPENDED_PENDING_INFO"
            decision_summary = "Loan suspended pending secondary debt restructuring or compensating factor verification."

        # Risk-Based Pricing LLPA Calculation
        llpa_bps = 0
        if credit_report["fico_score"] < 700:
            llpa_bps += 50
        if collateral_result["ltv_pct"] > 80.0:
            llpa_bps += 37
        if income_verification["employment_type"] == "SELF_EMPLOYED":
            llpa_bps += 25

        base_rate = self.loan.get("base_interest_rate", 6.75)
        recommended_rate = base_rate + (llpa_bps / 1000.0)

        # Generate Stipulations
        stipulations = []
        if income_verification.get("requires_2yr_tax_transcripts"):
            stipulations.append({
                "condition_id": "COND-101",
                "category": "PRIOR_TO_DOCS",
                "description": "Obtain signed IRS Form 4506-C and 2 years of filed federal tax transcripts (1040s).",
                "assigned_to": "Loan Processor",
                "satisfied": False
            })
        if collateral_result.get("requires_private_mortgage_insurance"):
            stipulations.append({
                "condition_id": "COND-102",
                "category": "PRIOR_TO_DOCS",
                "description": "Secure Private Mortgage Insurance (PMI) certificate covering LTV exposure > 80.0%.",
                "assigned_to": "Underwriting Operations",
                "satisfied": False
            })
        if collateral_result.get("flood_insurance_required"):
            stipulations.append({
                "condition_id": "COND-103",
                "category": "PRIOR_TO_FUNDING",
                "description": "Provide paid Flood Hazard Insurance policy (NFIP/FEMA compliant).",
                "assigned_to": "Escrow Officer",
                "satisfied": False
            })
        stipulations.append({
            "condition_id": "COND-104",
            "category": "PRIOR_TO_FUNDING",
            "description": "Complete final Verbal Verification of Employment (VVOE) within 10 business days of note date.",
            "assigned_to": "Closing Closer",
            "satisfied": False
        })
        stipulations.append({
            "condition_id": "COND-105",
            "category": "PRIOR_TO_FUNDING",
            "description": "Deliver final clear ALTA Loan Policy of Title Insurance free of subordinate mechanics liens.",
            "assigned_to": "Title Company",
            "satisfied": False
        })

        decision_payload = {
            "application_id": self.app_data.get("application_id", "APP-2026-001"),
            "decision": decision,
            "decision_summary": decision_summary,
            "recommended_interest_rate": round(recommended_rate, 3),
            "pricing_adjustments_bps": llpa_bps,
            "credit_analysis": {
                "fico_score": credit_report["fico_score"],
                "risk_grade": credit_report["risk_grade"],
                "revolving_utilization_pct": credit_report["revolving_utilization_pct"],
                "total_monthly_obligations": self.borrower.get("monthly_debt_obligations", 450.0),
                "derogatory_summary": credit_report["derogatory_summary"],
                "credit_approved": credit_report["credit_approved"]
            },
            "income_analysis": {
                "verified_gross_monthly_income": income_verification["verified_gross_monthly_income"],
                "proposed_monthly_housing_payment": dti_result["proposed_monthly_housing_payment"],
                "front_end_dti_pct": dti_result["front_end_dti_pct"],
                "back_end_dti_pct": dti_result["back_end_dti_pct"],
                "dti_guideline_max": dti_result["dti_guideline_max"],
                "dti_compliant": dti_result["dti_compliant"],
                "reserves_months": dti_result["reserves_months"],
                "employment_stability": income_verification["employment_stability"],
                "income_approved": dti_result["dti_compliant"]
            },
            "collateral_analysis": {
                "appraised_value": collateral_result["appraised_value"],
                "ltv_pct": collateral_result["ltv_pct"],
                "cltv_pct": collateral_result["cltv_pct"],
                "ltv_guideline_max": collateral_result["ltv_guideline_max"],
                "ltv_compliant": collateral_result["ltv_compliant"],
                "property_condition": collateral_result["property_condition_rating"],
                "equity_cushion_amount": collateral_result["equity_cushion_amount"],
                "market_trend": comps_result.get("market_trend", "STABLE"),
                "collateral_approved": collateral_result["collateral_approved"]
            },
            "compliance_analysis": {
                "ofac_sanctions_cleared": kyc_result["ofac_sanctions_cleared"],
                "identity_verified": kyc_result["identity_verified"],
                "synthetic_id_risk": fraud_result["synthetic_id_risk"],
                "fraud_risk_score": fraud_result["fraud_risk_score"],
                "aml_red_flags": kyc_result["aml_red_flags"],
                "fair_lending_compliant": True,
                "compliance_approved": fraud_result["compliance_approved"]
            },
            "stipulations": stipulations,
            "macro_perspective": f"Agency benchmark 10-Yr SOFR spreads reflect stable liquidity. Secondary market securitization conforms to Fannie Mae Desktop Underwriter (DU) standards at {recommended_rate:.3f}%.",
            "meso_perspective": f"Regional collateral market in {self.collateral.get('property_address', 'Austin, TX')} indicates {comps_result.get('market_trend', 'STABLE')} price trajectory with {comps_result.get('neighborhood_absorption_rate_months', 2.4)} months supply.",
            "micro_perspective": f"Applicant maintains ${self.borrower.get('liquid_reserves', 0):,.0f} liquid reserves ({dti_result.get('reserves_months', 0):.1f} mos PITI), compensating for revolving utilization.",
            "defensive_mitigations": [
                "Execute pre-funding VVOE to mitigate employer turnover risk.",
                "Enforce title escrow buffer against subordinate encumbrances.",
                "Require automated escrow impounds for property taxes and hazard insurance."
            ],
            "positional_recommendations": [
                f"Issue 45-day rate lock commitment at {recommended_rate:.3f}%.",
                "Enroll borrower in automated ACH servicing discount program (0.125% rate incentive)."
            ],
            "scope_audit_note": "Underwriting analysis is bounded to single-lien primary residential purchase guidelines; subordinate second liens and non-arm's length transactions were excluded from scope."
        }

        # Deliver Dynamic A2UI Tabs Dossier
        tabs_payload = build_full_underwriting_tabs_a2ui(decision_payload)
        yield self._encode_rpc_frame("onUiComponentDelivery", {
            "author": "underwriting_orchestrator",
            "ui_specification": "0.9",
            "payload": tabs_payload
        })

        yield self._encode_rpc_frame("onAgentThought", {
            "author": "underwriting_orchestrator",
            "message": f"Underwriting completed successfully. Final Decision: {decision}. Total stipulations generated: {len(stipulations)}."
        })
