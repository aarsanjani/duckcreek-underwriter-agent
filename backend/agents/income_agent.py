"""
Income and Employment Verification Specialist Subagent (ADK 2.x).
Evaluates borrower capacity, W-2/1099 continuity, Front-End & Back-End DTI, and reserve coverage.
"""

from google.adk.agents import LlmAgent
from backend.tools.income_tools import verify_income_and_employment, calculate_dti_and_cashflow
from backend.config import MODEL_ID, logger


def income_agent_before_callback(callback_context):
    """Lifecycle hook triggered before income_employment_agent execution."""
    agent_name = getattr(callback_context, "agent_name", "income_employment_agent")
    logger.info(f"Activated Specialist Worker: {agent_name}")
    return None


def income_agent_after_callback(callback_context):
    """Lifecycle hook triggered after income_employment_agent completes."""
    agent_name = getattr(callback_context, "agent_name", "income_employment_agent")
    logger.info(f"Completed Specialist Worker turn: {agent_name}")
    return None


INCOME_AGENT_INSTRUCTION = """
You are the Senior Income & Capacity Underwriting Specialist Agent in an enterprise loan underwriting system.
Your sole mission is to verify applicant earning capacity, cash flow sustainability, and DTI debt ratios.

OPERATIONAL WORKFLOW:
1. Extract the borrower's employer, job title, years of tenure, employment type, stated gross income, liquid reserves, requested loan amount, and monthly debt obligations.
2. Execute the `verify_income_and_employment` tool to validate earning continuity, employment stability, and self-employment haircuts.
3. Execute the `calculate_dti_and_cashflow` tool to compute proposed PITI housing payment, Front-End DTI (Housing Ratio), Back-End DTI (Total Debt Ratio), and reserve coverage months.
4. Synthesize the findings into a concise, deterministic Income & Capacity Evaluation Summary covering:
   - Verified Monthly Qualifying Income and employment stability tier
   - Proposed Monthly Housing Payment (PITI)
   - Front-End DTI vs Guideline Ceiling
   - Back-End DTI vs Guideline Ceiling
   - Liquid Reserve Coverage in months
   - Explicit Recommendation: Income/Capacity Approved or Denied (with key factors)

ISOLATION ENFORCEMENT:
You must focus exclusively on income, capacity, and DTI debt serviceability. Do not evaluate property appraisal or OFAC compliance.
Yield your findings clearly and terminate your turn naturally.
"""


def create_income_agent() -> LlmAgent:
    """Instantiates the Income & Employment Specialist Agent with strict Hub-and-Spoke isolation."""
    return LlmAgent(
        name="income_employment_agent",
        description="Specialist agent that verifies employment, analyzes cash flow, calculates Front/Back DTI ratios and reserve months.",
        instruction=INCOME_AGENT_INSTRUCTION,
        tools=[verify_income_and_employment, calculate_dti_and_cashflow],
        model=MODEL_ID,
        disallow_transfer_to_parent=True,
        disallow_transfer_to_peers=True,
        before_agent_callback=income_agent_before_callback,
        after_agent_callback=income_agent_after_callback
    )
