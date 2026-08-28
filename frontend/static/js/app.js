/**
 * LOANFLOW AI - MULTI-AGENT DYNAMIC UI & SSE PARSER ENGINE
 * Implements the Dynamic Component Factory, Predictive Handoff Glows, and Real-Time Telemetry Parser.
 */

class MultiAgentDynamicUiEngine {
    constructor() {
        this.streamApiUrl = "/api/chat/stream";
        this.chatTerminal = document.getElementById("chatTerminal");
        this.a2uiCanvas = document.getElementById("a2uiCanvas");
        this.canvasPlaceholder = document.getElementById("canvasPlaceholder");
        this.scenarioSelect = document.getElementById("scenarioSelect");
        this.runPipelineBtn = document.getElementById("runPipelineBtn");
        this.clearTerminalBtn = document.getElementById("clearTerminalBtn");
        this.statusLabel = document.getElementById("statusLabel");

        this.eventSource = null;
        this.activeAgentNode = null;

        this.customAppBtn = document.getElementById("customAppBtn");
        this.customAppModal = document.getElementById("customAppModal");
        this.closeModalBtn = document.getElementById("closeModalBtn");
        this.cancelModalBtn = document.getElementById("cancelModalBtn");
        this.customAppForm = document.getElementById("customAppForm");

        this.initEventListeners();
        this.loadScenarioDetails(this.scenarioSelect.value);
    }

    initEventListeners() {
        this.scenarioSelect.addEventListener("change", (e) => {
            this.loadScenarioDetails(e.target.value);
        });

        this.runPipelineBtn.addEventListener("click", () => {
            this.triggerUnderwritingPipeline();
        });

        if (this.customAppBtn) {
            this.customAppBtn.addEventListener("click", () => {
                this.customAppModal.style.display = "flex";
            });
        }

        if (this.closeModalBtn) {
            this.closeModalBtn.addEventListener("click", () => {
                this.customAppModal.style.display = "none";
            });
        }

        if (this.cancelModalBtn) {
            this.cancelModalBtn.addEventListener("click", () => {
                this.customAppModal.style.display = "none";
            });
        }

        if (this.customAppForm) {
            this.customAppForm.addEventListener("submit", (e) => {
                e.preventDefault();
                this.customAppModal.style.display = "none";
                this.triggerCustomUnderwritingPipeline();
            });
        }

        this.clearTerminalBtn.addEventListener("click", () => {
            this.chatTerminal.innerHTML = `
                <div class="terminal-welcome-msg">
                    <span class="timestamp">[SYSTEM CLEARED]</span> Log reset. Ready for next run.
                </div>
            `;
        });
    }

    triggerCustomUnderwritingPipeline() {
        const customData = {
            application_id: `APP-CUSTOM-${Date.now()}`,
            submission_timestamp: new Date().toISOString(),
            borrower: {
                borrower_id: `BW-${Date.now()}`,
                full_name: document.getElementById("custName").value,
                ssn_last4: "8899",
                dob: "1987-03-21",
                current_address: document.getElementById("custAddress").value,
                employment_type: document.getElementById("custEmpType").value,
                employer_name: "Apex Global Dynamics",
                job_title: "Operations Lead",
                years_at_employer: 3.5,
                years_in_profession: 8.0,
                stated_monthly_gross_income: parseFloat(document.getElementById("custIncome").value),
                monthly_debt_obligations: parseFloat(document.getElementById("custDebts").value),
                liquid_reserves: parseFloat(document.getElementById("custReserves").value),
                credit_score: parseInt(document.getElementById("custFico").value, 10),
                bankruptcy_flag: false,
                prior_foreclosure_flag: false,
                delinquencies_last_24m: 0,
                citizenship_status: "US_CITIZEN"
            },
            collateral: {
                property_id: `PROP-${Date.now()}`,
                property_address: document.getElementById("custAddress").value,
                property_type: "SINGLE_FAMILY",
                occupancy: "PRIMARY_RESIDENCE",
                purchase_price: parseFloat(document.getElementById("custPrice").value),
                appraised_value: parseFloat(document.getElementById("custAppraisal").value),
                automated_valuation_confidence: 0.95,
                property_condition_rating: "C2",
                flood_zone_risk: "ZONE_X_LOW",
                environmental_flag: false
            },
            loan: {
                loan_id: `LN-${Date.now()}`,
                loan_type: document.getElementById("custLoanType").value,
                purpose: "PURCHASE",
                requested_loan_amount: parseFloat(document.getElementById("custLoanAmt").value),
                loan_term_months: 360,
                base_interest_rate: parseFloat(document.getElementById("custRate").value),
                target_amortization_type: "FIXED_RATE"
            }
        };

        // Update quick glance panel
        document.getElementById("qBorrowerName").innerText = customData.borrower.full_name;
        document.getElementById("qLoanAmount").innerText = `$${customData.loan.requested_loan_amount.toLocaleString()}`;
        document.getElementById("qPropertyAddress").innerText = customData.collateral.property_address;
        document.getElementById("qStatedIncome").innerText = `$${customData.borrower.stated_monthly_gross_income.toLocaleString()} / mo`;
        const qFico = document.getElementById("qCreditScore");
        qFico.innerText = `${customData.borrower.credit_score} (${customData.borrower.credit_score >= 680 ? 'Prime' : 'Subprime'})`;
        qFico.className = customData.borrower.credit_score >= 680 ? "highlight-green" : "highlight-red";

        this.triggerUnderwritingPipelineWithData(customData);
    }

    async loadScenarioDetails(scenarioId) {
        try {
            const resp = await fetch(`/api/scenarios/${scenarioId}`);
            const result = await resp.json();
            if (result.status === "success") {
                const data = result.data;
                const b = data.borrower;
                const c = data.collateral;
                const l = data.loan;

                document.getElementById("qBorrowerName").innerText = b.full_name;
                document.getElementById("qLoanAmount").innerText = `$${l.requested_loan_amount.toLocaleString()}`;
                document.getElementById("qPropertyAddress").innerText = c.property_address;
                document.getElementById("qStatedIncome").innerText = `$${b.stated_monthly_gross_income.toLocaleString()} / mo`;
                
                const qFico = document.getElementById("qCreditScore");
                qFico.innerText = `${b.credit_score} (${b.credit_score >= 740 ? 'Prime+' : (b.credit_score >= 680 ? 'Prime' : 'Near/Sub')})`;
                qFico.className = b.credit_score >= 680 ? "highlight-green" : "highlight-red";
            }
        } catch (err) {
            console.error("Failed to load scenario details:", err);
        }
    }

    triggerUnderwritingPipeline() {
        const scenarioId = this.scenarioSelect.value;
        const sessionId = `session-${Date.now()}`;

        this.startStreamPipeline(sessionId, { scenario_id: scenarioId });
    }

    triggerUnderwritingPipelineWithData(customData) {
        const sessionId = `session-custom-${Date.now()}`;
        this.startStreamPipeline(sessionId, { application_data: customData });
    }

    startStreamPipeline(sessionId, payloadBody) {
        // Reset visual state
        this.resetAgentNodes();
        this.runPipelineBtn.disabled = true;
        this.runPipelineBtn.innerHTML = `<span class="btn-icon">⏳</span> Underwriting Active...`;
        this.statusLabel.innerText = "Orchestrating Subagents...";
        if (this.canvasPlaceholder) {
            this.canvasPlaceholder.style.display = "none";
        }

        // Close any active event source
        if (this.eventSource) {
            this.eventSource.close();
        }

        const triggerDesc = payloadBody.scenario_id ? `Scenario [${payloadBody.scenario_id}]` : `Custom Loan [${payloadBody.application_data.borrower.full_name}]`;
        this.appendTerminalLog("LeadUnderwritingOrchestrator", `Triggered Underwriting Cycle for ${triggerDesc} (Session: ${sessionId})`, "thought");

        // Light up orchestrator
        this.setAgentNodeState("underwriting_orchestrator", "active-turn", "ORCHESTRATING");

        // Establish SSE Connection via POST with custom payload if provided, or GET
        let streamUrl = "";
        if (payloadBody.scenario_id) {
            streamUrl = `${this.streamApiUrl}?scenario_id=${encodeURIComponent(payloadBody.scenario_id)}&session_id=${encodeURIComponent(sessionId)}`;
            this.eventSource = new EventSource(streamUrl);
            this.attachStreamHandlers();
        } else {
            // For custom data, use fetch with readable stream or post session init
            fetch(this.streamApiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    session_id: sessionId,
                    application_data: payloadBody.application_data
                })
            }).then(response => {
                const reader = response.body.getReader();
                const decoder = new TextDecoder("utf-8");
                let buffer = "";

                const readChunk = () => {
                    reader.read().then(({ done, value }) => {
                        if (done) {
                            this.onStreamComplete();
                            return;
                        }
                        buffer += decoder.decode(value, { stream: true });
                        const frames = buffer.split("\n\n");
                        buffer = frames.pop(); // Keep partial frame in buffer

                        for (const frame of frames) {
                            if (frame.startsWith("data:")) {
                                try {
                                    const jsonStr = frame.replace("data:", "").trim();
                                    const rpcFrame = JSON.parse(jsonStr);
                                    this.handleRpcFrame(rpcFrame);
                                } catch (e) {
                                    console.error("Malformed custom frame:", e);
                                }
                            }
                        }
                        readChunk();
                    }).catch(err => {
                        console.error("Stream read error:", err);
                        this.onStreamComplete();
                    });
                };
                readChunk();
            }).catch(err => {
                console.error("POST stream failed:", err);
                this.onStreamComplete();
            });
        }
    }

    attachStreamHandlers() {
        this.eventSource.onmessage = (event) => {
            try {
                const rpcFrame = JSON.parse(event.data);
                this.handleRpcFrame(rpcFrame);
            } catch (err) {
                console.error("Malformed SSE frame:", err, event.data);
            }
        };

        this.eventSource.onerror = (err) => {
            this.eventSource.close();
            this.onStreamComplete();
        };
    }

    onStreamComplete() {
        this.runPipelineBtn.disabled = false;
        this.runPipelineBtn.innerHTML = `<span class="btn-icon">▶</span> Run Underwriting Pipeline`;
        this.statusLabel.innerText = "Underwriting Completed";
        this.setAgentNodeState("underwriting_orchestrator", "", "COMPLETED");
    }

    handleRpcFrame(rpcFrame) {
        const { method, params } = rpcFrame;

        switch (method) {
            case "onAgentThought":
                this.appendTerminalLog(params.author, params.message, "thought");
                this.updateAgentIoSnippet(params.author, params.message);
                break;

            case "onAgentDelegation":
                // Predictive Handoff Neon Glow
                this.predictiveHandoffGlow(params.author, params.target);
                this.appendTerminalLog(params.author, `➜ Delegated control to [${params.target}]: ${params.message}`, "delegation");
                this.updateAgentIoSnippet(params.target, "Starting evaluation turn...");
                break;

            case "onToolCall":
                const argsStr = JSON.stringify(params.arguments);
                this.appendTerminalLog(params.author, `⚙ Invoked Tool [${params.tool}] with args: ${argsStr}`, "tool");
                this.updateAgentIoSnippet(params.author, `Tool: ${params.tool}()`);
                break;

            case "onUiComponentDelivery":
                this.renderDynamicUiComponent(params.payload);
                if (params.payload && params.payload.id === "underwriting_dossier_tabs") {
                    this.updateAgentIoSnippet("underwriting_orchestrator", "Completed Step C Synthesis");
                }
                break;

            case "onError":
                this.appendTerminalLog(params.author || "System", `❌ Error: ${params.error}`, "tool");
                break;

            default:
                console.warn("Unhandled RPC method:", method);
        }
    }

    updateAgentIoSnippet(agentName, text) {
        const ioElem = document.getElementById(`io-${agentName}`);
        if (ioElem && text) {
            // Trim and format text for snippet display
            let clean = text.replace(/^(Credit evaluation complete\.|Capacity verified\.|Collateral analysis complete\.|Compliance clearance completed\.)\s*/i, "");
            ioElem.innerText = clean.length > 38 ? clean.substring(0, 35) + "..." : clean;
        }
    }

    appendTerminalLog(author, message, type = "thought") {
        const row = document.createElement("div");
        row.className = `trace-bubble ${type}`;
        row.innerHTML = `<span class="trace-author">${author}:</span><span class="trace-content">${this.escapeHtml(message)}</span>`;
        this.chatTerminal.appendChild(row);
        this.chatTerminal.scrollTop = this.chatTerminal.scrollHeight;
    }

    predictiveHandoffGlow(sourceAgent, targetAgent) {
        // Set previous to completed/idle
        if (sourceAgent && sourceAgent !== "underwriting_orchestrator") {
            this.setAgentNodeState(sourceAgent, "", "IDLE");
        }

        // Set target node to activating glow immediately
        if (targetAgent) {
            this.setAgentNodeState(targetAgent, "activating", "ACTIVATING");
            setTimeout(() => {
                this.setAgentNodeState(targetAgent, "active-turn", "EXECUTING");
            }, 300);
        }
    }

    setAgentNodeState(agentName, cssClass, statusText) {
        const node = document.getElementById(`node-${agentName}`);
        const statusSpan = document.getElementById(`status-${agentName}`);

        if (node) {
            node.classList.remove("activating", "active-turn");
            if (cssClass) {
                node.classList.add(cssClass);
            }
        }
        if (statusSpan && statusText) {
            statusSpan.innerText = statusText;
        }
    }

    resetAgentNodes() {
        const workers = [
            "credit_analyst_agent",
            "income_employment_agent",
            "collateral_valuation_agent",
            "compliance_fraud_agent"
        ];
        workers.forEach(w => this.setAgentNodeState(w, "", "IDLE"));
        this.setAgentNodeState("underwriting_orchestrator", "", "STANDBY");
    }

    /**
     * DYNAMIC COMPONENT FACTORY
     * Renders Card, Tabs, Table, Badges, and Condition Lists
     */
    renderDynamicUiComponent(payload) {
        if (!payload) return;

        // If it's a Header Card or existing component, replace or append
        const existingNode = document.getElementById(payload.id);
        if (existingNode) {
            existingNode.remove();
        }

        let componentNode = null;

        if (payload.type === "Card") {
            componentNode = this.buildCardComponent(payload);
        } else if (payload.type === "Tabs") {
            componentNode = this.buildTabsComponent(payload);
        } else if (payload.type === "Table") {
            componentNode = this.buildTableComponent(payload);
        } else if (payload.type === "ConditionList") {
            componentNode = this.buildConditionListComponent(payload);
        }

        if (componentNode) {
            if (payload.id === "loan_header_summary") {
                this.a2uiCanvas.prepend(componentNode);
            } else {
                this.a2uiCanvas.appendChild(componentNode);
            }
        }
    }

    buildCardComponent(card) {
        const cardDiv = document.createElement("div");
        cardDiv.className = "a2ui-card";
        if (card.id) cardDiv.id = card.id;

        let headerHtml = "";
        if (card.title || card.subtitle || card.status_tag) {
            headerHtml = `
                <div class="a2ui-card-header">
                    <div class="a2ui-card-title-group">
                        <h2>${this.escapeHtml(card.title || '')}</h2>
                        ${card.subtitle ? `<div class="a2ui-card-subtitle">${this.escapeHtml(card.subtitle)}</div>` : ''}
                    </div>
                    ${card.status_tag ? `<span class="status-badge ${card.status_tag}">${card.status_tag.replace(/_/g, ' ')}</span>` : ''}
                </div>
            `;
        }

        let badgesHtml = "";
        if (card.badges && card.badges.length > 0) {
            badgesHtml = `<div class="a2ui-badges-grid">` + card.badges.map(b => `
                <div class="a2ui-metric-badge ${b.status || ''}">
                    <span class="a2ui-metric-label">${this.escapeHtml(b.label)}</span>
                    <span class="a2ui-metric-value">${this.escapeHtml(b.value)}</span>
                    ${b.subtext ? `<span class="a2ui-metric-subtext">${this.escapeHtml(b.subtext)}</span>` : ''}
                </div>
            `).join('') + `</div>`;
        }

        let contentHtml = card.content ? `<p class="a2ui-card-body-text">${this.escapeHtml(card.content)}</p>` : "";

        let kvHtml = "";
        if (card.key_value_pairs) {
            kvHtml = `<div class="a2ui-kv-grid">` + Object.entries(card.key_value_pairs).map(([k, v]) => `
                <div class="a2ui-kv-row">
                    <span class="a2ui-kv-key">${this.escapeHtml(k)}</span>
                    <span class="a2ui-kv-val">${this.escapeHtml(v)}</span>
                </div>
            `).join('') + `</div>`;
        }

        cardDiv.innerHTML = `${headerHtml}${badgesHtml}${contentHtml}${kvHtml}`;
        return cardDiv;
    }

    buildTabsComponent(tabs) {
        const wrapper = document.createElement("div");
        wrapper.className = "a2ui-tabs-wrapper a2ui-card";
        if (tabs.id) wrapper.id = tabs.id;

        const nav = document.createElement("div");
        nav.className = "a2ui-tabs-nav";

        const contentContainer = document.createElement("div");
        contentContainer.className = "a2ui-tabs-content-container";

        (tabs.components || []).forEach((item, idx) => {
            const btn = document.createElement("button");
            btn.className = `a2ui-tab-btn ${idx === 0 ? 'active' : ''}`;
            btn.innerText = item.title;
            btn.dataset.targetIndex = idx;

            const pane = document.createElement("div");
            pane.className = `a2ui-tab-pane ${idx === 0 ? 'active' : ''}`;
            pane.id = `tab-pane-${tabs.id || 'tabs'}-${idx}`;

            // Render inner component
            let innerNode = null;
            if (item.type === "Card") {
                innerNode = this.buildCardComponent(item);
            } else if (item.type === "Table") {
                innerNode = this.buildTableComponent(item);
            } else if (item.type === "ConditionList") {
                innerNode = this.buildConditionListComponent(item);
            }

            if (innerNode) pane.appendChild(innerNode);
            contentContainer.appendChild(pane);

            btn.addEventListener("click", () => {
                nav.querySelectorAll(".a2ui-tab-btn").forEach(b => b.classList.remove("active"));
                contentContainer.querySelectorAll(".a2ui-tab-pane").forEach(p => p.classList.remove("active"));
                btn.classList.add("active");
                pane.classList.add("active");
            });

            nav.appendChild(btn);
        });

        wrapper.appendChild(nav);
        wrapper.appendChild(contentContainer);
        return wrapper;
    }

    buildTableComponent(table) {
        const container = document.createElement("div");
        container.className = "a2ui-table-container";

        let headersHtml = "<tr>" + (table.headers || []).map(h => `<th>${this.escapeHtml(h)}</th>`).join('') + "</tr>";
        let rowsHtml = (table.rows || []).map(row => {
            return "<tr>" + row.map(cell => `<td>${this.escapeHtml(String(cell))}</td>`).join('') + "</tr>";
        }).join('');

        container.innerHTML = `
            <table class="a2ui-table">
                <thead>${headersHtml}</thead>
                <tbody>${rowsHtml}</tbody>
            </table>
        `;
        return container;
    }

    buildConditionListComponent(condList) {
        const listDiv = document.createElement("div");
        listDiv.className = "a2ui-condition-list";

        (condList.conditions || []).forEach(c => {
            const item = document.createElement("div");
            item.className = "a2ui-condition-item";
            item.innerHTML = `
                <div class="condition-check-box">✓</div>
                <div class="condition-details">
                    <div class="condition-desc"><strong>[${c.category}]</strong> ${this.escapeHtml(c.description)}</div>
                    <div class="condition-meta">Assigned To: ${this.escapeHtml(c.assigned_to)} | ID: ${c.condition_id}</div>
                </div>
            `;
            listDiv.appendChild(item);
        });

        return listDiv;
    }

    escapeHtml(str) {
        if (!str) return "";
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}

// Bootstrap UI Engine on DOM Load
document.addEventListener("DOMContentLoaded", () => {
    window.loanFlowUiEngine = new MultiAgentDynamicUiEngine();
});
