"""
Pre-loaded realistic loan application scenarios for dynamic testing and interactive demos.
"""

from typing import Dict, Any, List

SAMPLE_LOAN_APPLICATIONS: Dict[str, Dict[str, Any]] = {
    "APP-CONV-2026": {
        "application_id": "APP-CONV-2026",
        "submission_timestamp": "2026-08-28T14:00:00Z",
        "borrower": {
            "borrower_id": "BW-8801",
            "full_name": "Elena Rostova",
            "ssn_last4": "4821",
            "dob": "1989-04-12",
            "current_address": "450 South Congress Ave, Austin, TX 78704",
            "employment_type": "W2_EMPLOYED",
            "employer_name": "NextGen Cloud Platforms Inc",
            "job_title": "Principal Cloud Architect",
            "years_at_employer": 4.5,
            "years_in_profession": 11.0,
            "stated_monthly_gross_income": 16500.0,
            "monthly_debt_obligations": 550.0,
            "liquid_reserves": 95000.0,
            "credit_score": 765,
            "bankruptcy_flag": False,
            "prior_foreclosure_flag": False,
            "delinquencies_last_24m": 0,
            "citizenship_status": "US_CITIZEN"
        },
        "collateral": {
            "property_id": "PROP-TX-104",
            "property_address": "1204 Barton Springs Rd, Austin, TX 78704",
            "property_type": "SINGLE_FAMILY",
            "occupancy": "PRIMARY_RESIDENCE",
            "purchase_price": 680000.0,
            "appraised_value": 695000.0,
            "automated_valuation_confidence": 0.96,
            "property_condition_rating": "C2",
            "flood_zone_risk": "ZONE_X_LOW",
            "environmental_flag": False
        },
        "loan": {
            "loan_id": "LN-2026-8801",
            "loan_type": "CONVENTIONAL",
            "purpose": "PURCHASE",
            "requested_loan_amount": 544000.0,
            "loan_term_months": 360,
            "base_interest_rate": 6.625,
            "target_amortization_type": "FIXED_RATE"
        }
    },
    "APP-JUMBO-2026": {
        "application_id": "APP-JUMBO-2026",
        "submission_timestamp": "2026-08-28T14:05:00Z",
        "borrower": {
            "borrower_id": "BW-9402",
            "full_name": "Marcus Vance",
            "ssn_last4": "9934",
            "dob": "1983-11-20",
            "current_address": "220 Presidio Ave, San Francisco, CA 94115",
            "employment_type": "W2_EMPLOYED",
            "employer_name": "Autonomous AI Labs",
            "job_title": "VP of AI Systems",
            "years_at_employer": 3.0,
            "years_in_profession": 15.0,
            "stated_monthly_gross_income": 32000.0,
            "monthly_debt_obligations": 1800.0,
            "liquid_reserves": 320000.0,
            "credit_score": 795,
            "bankruptcy_flag": False,
            "prior_foreclosure_flag": False,
            "delinquencies_last_24m": 0,
            "citizenship_status": "US_CITIZEN"
        },
        "collateral": {
            "property_id": "PROP-CA-902",
            "property_address": "1540 Pacific Ave, San Francisco, CA 94109",
            "property_type": "SINGLE_FAMILY",
            "occupancy": "PRIMARY_RESIDENCE",
            "purchase_price": 1850000.0,
            "appraised_value": 1900000.0,
            "automated_valuation_confidence": 0.94,
            "property_condition_rating": "C1",
            "flood_zone_risk": "ZONE_X_LOW",
            "environmental_flag": False
        },
        "loan": {
            "loan_id": "LN-2026-9402",
            "loan_type": "JUMBO",
            "purpose": "PURCHASE",
            "requested_loan_amount": 1387500.0,
            "loan_term_months": 360,
            "base_interest_rate": 6.875,
            "target_amortization_type": "FIXED_RATE"
        }
    },
    "APP-SELFEMP-2026": {
        "application_id": "APP-SELFEMP-2026",
        "submission_timestamp": "2026-08-28T14:10:00Z",
        "borrower": {
            "borrower_id": "BW-3310",
            "full_name": "Sophia Morales",
            "ssn_last4": "3318",
            "dob": "1991-08-05",
            "current_address": "880 Brickell Key Dr, Miami, FL 33131",
            "employment_type": "SELF_EMPLOYED",
            "employer_name": "Morales Design & Architecture LLC",
            "job_title": "Managing Principal",
            "years_at_employer": 5.0,
            "years_in_profession": 9.0,
            "stated_monthly_gross_income": 19000.0,
            "monthly_debt_obligations": 950.0,
            "liquid_reserves": 80000.0,
            "credit_score": 730,
            "bankruptcy_flag": False,
            "prior_foreclosure_flag": False,
            "delinquencies_last_24m": 0,
            "citizenship_status": "PERMANENT_RESIDENT"
        },
        "collateral": {
            "property_id": "PROP-FL-401",
            "property_address": "320 Ocean Dr, Miami Beach, FL 33139",
            "property_type": "CONDOMINIUM",
            "occupancy": "PRIMARY_RESIDENCE",
            "purchase_price": 750000.0,
            "appraised_value": 760000.0,
            "automated_valuation_confidence": 0.92,
            "property_condition_rating": "C2",
            "flood_zone_risk": "ZONE_AE_HIGH",
            "environmental_flag": False
        },
        "loan": {
            "loan_id": "LN-2026-3310",
            "loan_type": "CONVENTIONAL",
            "purpose": "PURCHASE",
            "requested_loan_amount": 600000.0,
            "loan_term_months": 360,
            "base_interest_rate": 6.75,
            "target_amortization_type": "FIXED_RATE"
        }
    },
    "APP-ELEVATED-RISK": {
        "application_id": "APP-ELEVATED-RISK",
        "submission_timestamp": "2026-08-28T14:15:00Z",
        "borrower": {
            "borrower_id": "BW-1109",
            "full_name": "David Sterling",
            "ssn_last4": "7712",
            "dob": "1985-02-17",
            "current_address": "772 Peachtree St NE, Atlanta, GA 30308",
            "employment_type": "W2_EMPLOYED",
            "employer_name": "Metro Logistics Group",
            "job_title": "Fleet Supervisor",
            "years_at_employer": 1.2,
            "years_in_profession": 3.0,
            "stated_monthly_gross_income": 6200.0,
            "monthly_debt_obligations": 1400.0,
            "liquid_reserves": 8000.0,
            "credit_score": 605,
            "bankruptcy_flag": False,
            "prior_foreclosure_flag": False,
            "delinquencies_last_24m": 3,
            "citizenship_status": "US_CITIZEN"
        },
        "collateral": {
            "property_id": "PROP-GA-502",
            "property_address": "844 Piedmont Ave, Atlanta, GA 30308",
            "property_type": "SINGLE_FAMILY",
            "occupancy": "PRIMARY_RESIDENCE",
            "purchase_price": 420000.0,
            "appraised_value": 410000.0,
            "automated_valuation_confidence": 0.88,
            "property_condition_rating": "C4",
            "flood_zone_risk": "ZONE_X_LOW",
            "environmental_flag": False
        },
        "loan": {
            "loan_id": "LN-2026-1109",
            "loan_type": "CONVENTIONAL",
            "purpose": "PURCHASE",
            "requested_loan_amount": 395000.0,
            "loan_term_months": 360,
            "base_interest_rate": 7.25,
            "target_amortization_type": "FIXED_RATE"
        }
    }
}


def get_sample_application(app_id: str = "APP-CONV-2026") -> Dict[str, Any]:
    """Fetches a pre-configured sample loan application."""
    return SAMPLE_LOAN_APPLICATIONS.get(app_id, SAMPLE_LOAN_APPLICATIONS["APP-CONV-2026"])


def list_sample_scenarios() -> List[Dict[str, Any]]:
    """Returns summary metadata for all pre-configured scenarios."""
    return [
        {
            "id": k,
            "borrower_name": v["borrower"]["full_name"],
            "loan_type": v["loan"]["loan_type"],
            "loan_amount": v["loan"]["requested_loan_amount"],
            "property_location": v["collateral"]["property_address"],
            "credit_score": v["borrower"]["credit_score"],
            "description": f"{v['loan']['loan_type']} ${v['loan']['requested_loan_amount']:,.0f} - {v['borrower']['full_name']} (FICO {v['borrower']['credit_score']})"
        }
        for k, v in SAMPLE_LOAN_APPLICATIONS.items()
    ]
