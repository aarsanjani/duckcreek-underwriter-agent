"""
Backend Orchestration Service & Reactive Streaming Controller for Loan Underwriting.
Implements the Enterprise Supervisor Architecture, Runtime Stabilization, and JSON-RPC 2.0 SSE Streaming.
"""

import sys
import os
import json
import logging
from typing import Generator, Dict, Any
from flask import Flask, Response, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

# ==============================================================================
# PATTERN: RUNTIME ENVIRONMENT STABILIZATION (MONKEYPATCHING BOUNDARY)
# Dynamically resolves decoupled framework structural drift at startup.
# ==============================================================================
try:
    import a2a.types
    if not hasattr(a2a.types, "DataPart") or not hasattr(a2a.types, "TextPart"):
        logging.warning("Import drift detected in agentic SDK types. Applying stabilization proxy.")
        setattr(a2a.types, "DataPart", type("DataPart", (object,), {"__init__": lambda s, d: setattr(s, "data", d)}))
        setattr(a2a.types, "TextPart", type("TextPart", (object,), {"__init__": lambda s, t: setattr(s, "text", t)}))
except Exception as exc:
    logging.info(f"Runtime stabilization check: {exc}")

from backend.config import PROJECT_ID, LOCATION, MODEL_ID, logger
from backend.agents.orchestrator import ReactiveUnderwritingExecutionEngine, create_underwriting_orchestrator
from backend.workflows.sample_data import get_sample_application, list_sample_scenarios, SAMPLE_LOAN_APPLICATIONS

# Resolve directory paths for Flask templates & static assets
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE_DIR = os.path.join(BASE_DIR, "frontend", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app)


# ==============================================================================
# VIEW & STATIC ASSET ROUTES
# ==============================================================================
@app.route("/")
def index():
    """Serves the Glassmorphic Single-Page Loan Underwriting Cockpit."""
    return render_template("index.html")


@app.route("/static/<path:filename>")
def serve_static(filename):
    """Serves static JavaScript, CSS, and UI assets."""
    return send_from_directory(STATIC_DIR, filename)


# ==============================================================================
# API ENDPOINTS: SESSION & SCENARIOS
# ==============================================================================
@app.route("/api/session", methods=["GET"])
def session_context_manager() -> Response:
    """Manages active durable session context and metadata."""
    session_id = request.args.get("session_id", "session-underwrite-001")
    return jsonify({
        "session_id": session_id,
        "lifecycle_state": "ACTIVE",
        "project_id": PROJECT_ID,
        "location": LOCATION,
        "model_id": MODEL_ID,
        "ttl": 3600
    })


@app.route("/api/scenarios", methods=["GET"])
def get_scenarios() -> Response:
    """Returns available pre-configured loan underwriting application scenarios."""
    return jsonify({
        "status": "success",
        "scenarios": list_sample_scenarios()
    })


@app.route("/api/scenarios/<scenario_id>", methods=["GET"])
def get_scenario_detail(scenario_id: str) -> Response:
    """Returns full borrower, loan, and collateral data for a selected scenario."""
    if scenario_id in SAMPLE_LOAN_APPLICATIONS:
        return jsonify({
            "status": "success",
            "scenario_id": scenario_id,
            "data": SAMPLE_LOAN_APPLICATIONS[scenario_id]
        })
    return jsonify({"status": "error", "message": f"Scenario {scenario_id} not found."}), 404


# ==============================================================================
# PATTERN: REACTIVE STREAMING CONTROLLER
# Controller layer converting multi-agent execution events into a persistent SSE stream.
# ==============================================================================
@app.route("/api/chat/stream", methods=["POST", "GET"])
def reactive_stream_endpoint() -> Response:
    """
    Consumes loan underwriting request payloads and streams real-time JSON-RPC 2.0 telemetry frames over SSE.
    """
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
        scenario_id = payload.get("scenario_id", "APP-CONV-2026")
        custom_app_data = payload.get("application_data")
        session_id = payload.get("session_id", "session-underwrite-001")
        prompt = payload.get("prompt", "")
    else:
        scenario_id = request.args.get("scenario_id", "APP-CONV-2026")
        custom_app_data = None
        session_id = request.args.get("session_id", "session-underwrite-001")
        prompt = request.args.get("prompt", "")

    # Load application payload
    if custom_app_data and isinstance(custom_app_data, dict):
        loan_app = custom_app_data
    else:
        loan_app = get_sample_application(scenario_id)

    # Initialize the Reactive Underwriting Execution Engine
    engine = ReactiveUnderwritingExecutionEngine(
        session_id=session_id,
        loan_application_data=loan_app
    )

    def sse_event_encoder() -> Generator[str, None, None]:
        try:
            for trace_frame in engine.execute_workflow_stream():
                yield f"data: {trace_frame}\n\n"
        except Exception as err:
            logger.error(f"Error during streaming execution: {err}", exc_info=True)
            error_rpc = json.dumps({
                "jsonrpc": "2.0",
                "method": "onError",
                "params": {"error": str(err), "author": "underwriting_orchestrator"}
            })
            yield f"data: {error_rpc}\n\n"

    return Response(
        sse_event_encoder(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Prevents reverse proxy buffering
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    logger.info(f"Starting Loan Underwriting Multi-Agent Service on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
