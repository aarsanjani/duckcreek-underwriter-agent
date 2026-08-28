"""
Credit Analyst Specialist Subagent (ADK 2.x).
Evaluates credit reports, FICO tiers, payment history, derogatory marks, and debt obligations.
"""

from google.adk.agents import LlmAgent
from backend.tools.credit_tools import fetch_credit_report, analyze_debt_obligations
from backend.config import MODEL_ID, logger


def credit_agent_before_callback(callback_context):
    """Lifecycle hook triggered before credit_analyst_agent execution."""
    agent_name = getattr(callback_context, "agent_name", "credit_analyst_agent")
    logger.info(f"Activated Specialist Worker: {agent_name}")
    return None


def credit_agent_after_callback(callback_context):
    """Lifecycle hook triggered after credit_analyst_agent completes."""
    agent_name = getattr(callback_context, "agent_name", "credit_analyst_agent")
    logger.info(f"Completed Specialist Worker turn: {agent_name}")
    return None


CREDIT_AGENT_INSTRUCTION = """
You are the Senior Credit Analyst Specialist Agent in an enterprise loan underwriting system.
Your sole mission is to execute exhaustive credit risk evaluations on the applicant.

OPERATIONAL WORKFLOW:
1. Extract the borrower's identifier, credit score, delinquencies, bankruptcy status, and monthly debt obligations.
2. Execute the `fetch_credit_report` tool with the applicant's parameters to obtain official bureau findings.
3. Execute the `analyze_debt_obligations` tool to assess non-housing leverage and revolving balance risks.
4. Synthesize the findings into a concise, deterministic Credit Evaluation Summary covering:
   - FICO Score and Prime/Subprime Risk Grade
   - Payment history integrity and derogatory seasoning
   - Revolving credit utilization and debt service stability
   - Explicit Recommendation: Credit Approved or Credit Denied (with key factors)

ISOLATION ENFORCEMENT:
You must focus exclusively on credit analysis. Do not evaluate property appraisal, income DTI, or KYC compliance.
Yield your findings clearly and terminate your turn naturally.
"""


def create_credit_agent() -> LlmAgent:
    """Instantiates the Credit Analyst Specialist Agent with strict Hub-and-Spoke isolation."""
    return LlmAgent(
        name="credit_analyst_agent",
        description="Specialist agent that analyzes credit history, FICO score, delinquencies, and debt obligations.",
        instruction=CREDIT_AGENT_INSTRUCTION,
        tools=[fetch_credit_report, analyze_debt_obligations],
        model=MODEL_ID,
        disallow_transfer_to_parent=True,  # Prevents worker from commandeering root orchestrator
        disallow_transfer_to_peers=True,   # Prevents lateral hops between worker agents
        before_agent_callback=credit_agent_before_callback,
        after_agent_callback=credit_agent_after_callback
    )
