"""
Integration tests for the Reactive Streaming Controller, SSE format, and JSON-RPC 2.0 Schema Compliance.
Adheres strictly to the test harness specification in architecture.md.
"""

import json
import pytest
from backend.app import app


@pytest.fixture
def client_test_harness():
    """Configures the Flask test harness with isolated sandbox testing flags."""
    app.config["TESTING"] = True
    with app.test_client() as harness:
        yield harness


def test_session_endpoint(client_test_harness):
    """Verifies that the session context manager endpoint returns durable session status."""
    resp = client_test_harness.get("/api/session?session_id=test-sess-100")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["session_id"] == "test-sess-100"
    assert data["lifecycle_state"] == "ACTIVE"


def test_scenarios_endpoint(client_test_harness):
    """Verifies retrieval of pre-configured sample loan application scenarios."""
    resp = client_test_harness.get("/api/scenarios")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "success"
    assert len(data["scenarios"]) >= 4


def test_scenario_detail_endpoint(client_test_harness):
    """Verifies retrieval of scenario specific borrower and collateral details."""
    resp = client_test_harness.get("/api/scenarios/APP-CONV-2026")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "success"
    assert "borrower" in data["data"]
    assert "collateral" in data["data"]
    assert "loan" in data["data"]


def test_stream_endpoint_schema_compliance(client_test_harness):
    """
    Verifies that the SSE streaming pipeline returns compliant content types
    and valid JSON-RPC 2.0 event blocks conforming to architecture.md.
    """
    payload = {
        "scenario_id": "APP-CONV-2026",
        "session_id": "sandbox-test-stream-01",
        "prompt": "Run full multi-agent underwriting pipeline"
    }
    resp = client_test_harness.post("/api/chat/stream", json=payload)
    
    assert resp.status_code == 200
    assert "text/event-stream" in resp.headers["Content-Type"]
    
    raw_text = resp.get_data(as_text=True)
    assert len(raw_text) > 0

    lines = [line.strip() for line in raw_text.split("\n\n") if line.strip()]
    assert len(lines) >= 8  # Multiple frames emitted for sequential turns + A2UI delivery

    methods_encountered = set()
    a2ui_components_delivered = []

    for frame in lines:
        assert frame.startswith("data:")
        json_str = frame.replace("data:", "").strip()
        rpc_obj = json.loads(json_str)

        assert rpc_obj["jsonrpc"] == "2.0"
        assert "method" in rpc_obj
        assert "params" in rpc_obj

        method = rpc_obj["method"]
        methods_encountered.add(method)

        if method == "onUiComponentDelivery":
            a2ui_components_delivered.append(rpc_obj["params"]["payload"])

    # Ensure all core lifecycle methods were emitted in the multi-agent execution
    assert "onAgentThought" in methods_encountered
    assert "onAgentDelegation" in methods_encountered
    assert "onToolCall" in methods_encountered
    assert "onUiComponentDelivery" in methods_encountered

    # Verify A2UI schema payloads
    component_types = [c.get("type") for c in a2ui_components_delivered]
    assert "Card" in component_types
    assert "Tabs" in component_types
