"""
Compliance, KYC/AML & Anti-Fraud Specialist Subagent (ADK 2.x).
Performs OFAC sanctions screening, Customer Identification Program (CIP) checks, and fraud anomaly detection.
"""

from google.adk.agents import LlmAgent
from backend.tools.compliance_tools import run_kyc_aml_sanctions_check, detect_fraud_indicators
from backend.config import MODEL_ID, logger


def compliance_agent_before_callback(callback_context):
    """Lifecycle hook triggered before compliance_fraud_agent execution."""
    agent_name = getattr(callback_context, "agent_name", "compliance_fraud_agent")
    logger.info(f"Activated Specialist Worker: {agent_name}")
    return None


def compliance_agent_after_callback(callback_context):
    """Lifecycle hook triggered after compliance_fraud_agent completes."""
    agent_name = getattr(callback_context, "agent_name", "compliance_fraud_agent")
    logger.info(f"Completed Specialist Worker turn: {agent_name}")
    return None


COMPLIANCE_AGENT_INSTRUCTION = """
You are the Senior Compliance, Regulatory & Anti-Fraud Specialist Agent in an enterprise loan underwriting system.
Your sole mission is to ensure rigorous regulatory compliance (KYC, OFAC, AML, ECOA, Red Flags Rule) and detect financial fraud risks.

OPERATIONAL WORKFLOW:
1. Extract the borrower's legal name, SSN last 4, date of birth, residential address, citizenship status, stated income, and appraisal details.
2. Execute the `run_kyc_aml_sanctions_check` tool to screen OFAC SDN lists, verify identity credentials, and assess PEP status.
3. Execute the `detect_fraud_indicators` tool to run heuristic fraud anomaly checks (income inflation, appraisal gaps, rapid credit shifts).
4. Synthesize the findings into a concise, deterministic Compliance Evaluation Summary covering:
   - OFAC/Sanctions Watchlist clearance status
   - CIP Identity Verification and citizenship status
   - Fraud Risk Score (0-100) and Synthetic ID Risk tier
   - Detected AML / Red Flag anomalies
   - Explicit Recommendation: Compliance Cleared or Escalation Required

ISOLATION ENFORCEMENT:
You must focus exclusively on regulatory compliance, KYC/AML, and anti-fraud analysis. Do not evaluate LTV or DTI calculations.
Yield your findings clearly and terminate your turn naturally.
"""


def create_compliance_agent() -> LlmAgent:
    """Instantiates the Compliance & Fraud Specialist Agent with strict Hub-and-Spoke isolation."""
    return LlmAgent(
        name="compliance_fraud_agent",
        description="Specialist agent that performs OFAC watchlist screening, KYC identity verification, and anti-fraud detection.",
        instruction=COMPLIANCE_AGENT_INSTRUCTION,
        tools=[run_kyc_aml_sanctions_check, detect_fraud_indicators],
        model=MODEL_ID,
        disallow_transfer_to_parent=True,
        disallow_transfer_to_peers=True,
        before_agent_callback=compliance_agent_before_callback,
        after_agent_callback=compliance_agent_after_callback
    )
