"""
Application Entrypoint for the Loan Underwriting Multi-Agent System.
"""

import os
from backend.app import app
from backend.config import logger

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    logger.info(f"⚡ Launching LoanFlow AI Underwriting Multi-Agent System on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
