"""
Collateral Valuation & Property Risk Specialist Subagent (ADK 2.x).
Evaluates property appraisals, LTV/CLTV ratios, market comparables, condition ratings, and hazard zones.
"""

from google.adk.agents import LlmAgent
from backend.tools.collateral_tools import appraise_collateral_and_ltv, evaluate_market_comparables
from backend.config import MODEL_ID, logger


def collateral_agent_before_callback(callback_context):
    """Lifecycle hook triggered before collateral_valuation_agent execution."""
    agent_name = getattr(callback_context, "agent_name", "collateral_valuation_agent")
    logger.info(f"Activated Specialist Worker: {agent_name}")
    return None


def collateral_agent_after_callback(callback_context):
    """Lifecycle hook triggered after collateral_valuation_agent completes."""
    agent_name = getattr(callback_context, "agent_name", "collateral_valuation_agent")
    logger.info(f"Completed Specialist Worker turn: {agent_name}")
    return None


COLLATERAL_AGENT_INSTRUCTION = """
You are the Senior Collateral Valuation & Appraisal Specialist Agent in an enterprise loan underwriting system.
Your sole mission is to assess the property asset value, calculate LTV/CLTV ratios, and evaluate collateral risk.

OPERATIONAL WORKFLOW:
1. Extract the property address, property type, occupancy status, purchase price, appraised value, requested loan amount, condition rating, and flood zone.
2. Execute the `appraise_collateral_and_ltv` tool to verify valuation basis, compute LTV and CLTV percentages, and check guideline thresholds.
3. Execute the `evaluate_market_comparables` tool to check neighborhood absorption velocity and price trend stability.
4. Synthesize the findings into a concise, deterministic Collateral Evaluation Summary covering:
   - Appraised Value vs Contract Purchase Price (Valuation Basis)
   - Calculated LTV & CLTV percentages vs Guideline Maximum
   - Equity cushion dollar amount and Private Mortgage Insurance (PMI) requirement
   - Property condition rating (C1-C6) and flood insurance requirements
   - Explicit Recommendation: Collateral Approved or Denied (with key factors)

ISOLATION ENFORCEMENT:
You must focus exclusively on property appraisal, collateral adequacy, and market risk. Do not evaluate credit scores or KYC clearance.
Yield your findings clearly and terminate your turn naturally.
"""


def create_collateral_agent() -> LlmAgent:
    """Instantiates the Collateral Valuation Specialist Agent with strict Hub-and-Spoke isolation."""
    return LlmAgent(
        name="collateral_valuation_agent",
        description="Specialist agent that appraises collateral, calculates LTV/CLTV ratios, and evaluates property condition and market trends.",
        instruction=COLLATERAL_AGENT_INSTRUCTION,
        tools=[appraise_collateral_and_ltv, evaluate_market_comparables],
        model=MODEL_ID,
        disallow_transfer_to_parent=True,
        disallow_transfer_to_peers=True,
        before_agent_callback=collateral_agent_before_callback,
        after_agent_callback=collateral_agent_after_callback
    )
