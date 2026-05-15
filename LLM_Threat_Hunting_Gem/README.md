# 🧠 LLM Threat Hunting Gem

## Overview
This custom AI-driven tool was engineered to accelerate the Cyber Incident Response Team (CIRT) triage pipeline. It parses raw cyber threat intelligence (CTI), extracts actionable indicators of compromise (IoCs), and maps adversary behaviors to the MITRE ATT&CK framework.

## The Problem
Manually parsing OSINT reports, extracting indicators, and writing SIEM queries (SPL/YARA-L) to hunt for emerging zero-days across a high log volume environment was taking 30-45 minutes per critical alert.

## The Solution
I developed this custom LLM architecture with heavily engineered system prompts to:
1. Ingest raw CTI (PDFs, blogs, raw text).
2. Automatically extract network and host-based indicators.
3. Generate syntactically correct queries for Splunk and Google SecOps.
4. Output a standardized Markdown summary for executive CIRT briefings.

## Impact
* **Reduced Mean-Time-To-Triage (MTTT)** for complex threat hunts significantly.
* Eliminated syntax errors in high-stress, rapid-response query generation.
* Standardized IR reporting across the global team.

*(Note: The system prompts and architecture logic below have been sanitized to remove proprietary enterprise data.)*

---

## 🏗️ Architecture & Implementation
This Gem utilizes an advanced system prompt orchestration model coupled with schema enforcement to guarantee that generated queries strictly map to enterprise SIEM/XDR datasets (such as Google SecOps UDM or Palo Alto Cortex XQL) without introducing LLM hallucinations.

### 🛑 Core Prompt Engineering & System Logic
The core engine has been architected as an Object-Oriented Python application (`main.py`). 

To enforce strict query-writing guardrails and eliminate LLM hallucinations without blowing up token limits, this Gem utilizes the **Google GenAI File API**. By uploading massive SIEM schema guides (e.g., Google SecOps UDM and Palo Alto Cortex XQL dictionaries) as direct context files, the LLM maintains perfect data model compliance during generation.

**Key Files to Review:**
* `main.py`: The core stateful application logic and API orchestration.
* `system_prompt.txt`: The engineered guardrails, persona definition, and multi-phase execution instructions.

## 📋 The Stateful Logic Pipeline
The Gem operates across three deterministic phases to ensure quality control from threat ingestion to the final incident response brief:

## Phase 1: Hunt Report Generation
Upon tracking an adversary or malware campaign, the engine isolates host and network-level indicators to generate a full-text Incident Response Hunt Report template, complete with valid schema queries:

```sql
// Example of generated UDM query for tracking anomalous Process Injections
$event.metadata.event_type = "PROCESS_INJECTION"
$event.principal.process.file.full_path = /.*\\powershell\.exe/ or $event.principal.process.file.full_path = /.*\\cmd\.exe/
$event.target.process.pid = $target_pid
```

## Phase 2: Result Analysis Mode
Triggered dynamically when a user provides data matching the output of the hunting queries. The engine switches into an analytics triage assistant, filtering out known benign administrative behaviors from actual malicious activity based on user environment metadata.

## Phase 3: Conclusion & Executive Summary
Aggregates query output counts, verified true-positive indicators, and containment timelines into a concise, non-technical brief prepared directly for the CISO or security leadership.