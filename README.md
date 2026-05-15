# 🛡️ Detection Engineering & Threat Hunting Portfolio
**Author:** Edward Trimble (@dfir-g0blin) | **Role:** Staff Security Engineer, CIRT Lead

Welcome to my portfolio. This repository contains a curated, sanitized collection of detection logic, threat hunting playbooks, and AI-assisted security automation I have architected for massive-scale enterprise environments (100k+ endpoints, 200TB/week log volume).

> ⚠️ **Notice:** All code and logic in this repository has been strictly anonymized. Internal IPs, domains, and proprietary naming conventions have been replaced with generic variables (e.g., `<INTERNAL_SUBNET>`, `<CORP_DOMAIN>`).

## 🧠 Highlight: LLM "Threat Hunting Gem"
Located in `/LLM_Threat_Hunting_Gem/`
A custom-engineered tool leveraging LLM architecture to accelerate incident response.
* **Use Case:** Automates the parsing of raw cyber threat intelligence (CTI) into actionable hunt parameters.
* **Impact:** Drastically reduces mean-time-to-triage (MTTT) and standardizes complex IR reporting for executive leadership.

## 🎯 Detection Engineering (Sigma / YARA-L / SPL)
Located in `/Detection_Engineering/`
High-fidelity detection logic engineered to hunt advanced persistent threats (APTs) and zero-day exploitation. Focuses on minimizing false positives while maintaining deep visibility across hybrid cloud environments (Azure/GCP).
* **CVE-2026-20182 (Cisco SD-WAN):** Custom logic for detecting auth bypass attempts.
* **Supply Chain Compromise:** Detections mapped to MITRE ATT&CK targeting third-party vendor risks.

## ⚙️ SOAR & Automation
Located in `/Automation_Playbooks/`
Playbooks and scripts designed to pivot from SIEM/EDR alerts to automated containment and evidence collection.
