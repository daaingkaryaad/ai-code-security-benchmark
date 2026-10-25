# AI-Generated Code Security Benchmark

**Team members:** Ingkar Adilbek and Dinara Dyussembayeva  
**Group:** SE-2424  

## Research Question

How do the types and frequencies of security vulnerabilities in AI-generated code vary across Python, Java, and JavaScript when the same task types are evaluated under comparable generation and assessment conditions?

## Project Overview

This study examines AI-generated code across three programming languages and three task domains: database access, file handling, and authentication.

The dataset contains **18** final code samples from six matched programming tasks, with one generation per task and language. An additional **9 pilot samples** were collected separately.

Code was generated using **GPT-6 with Medium thinking** through the ChatGPT web interface.

Security analysis was performed using **Semgrep Community Edition 1.182.0**, targeting CWE-89, CWE-22, CWE-256, and CWE-798. The automated scans reported zero findings across the 18 final samples and nine pilot samples. Source-code assessment records are maintained separately.

## Project Structure

| Directory | Contents |
|---|---|
| `prompts/` | Programming task prompts |
| `protocol/` | Task definitions, collection schedule, and data dictionary |
| `scripts/` | Code collection scripts |
| `data/source/` | Generated Python, Java, and JavaScript code |
| `data/raw/` | Saved model responses |
| `data/processed/` | Semgrep scan results |
| `assessment/` | CWE checklist and review records |
| `logs/` | Collection logs |
| `evidence/` | Screenshots of generation and testing |
| `fixtures/` | Test data and database fixtures |

## Collection and Evaluation

The final dataset is located in `data/source/final-web-v1/`. The separate pilot dataset is stored in `data/source/pilot-web-v1/`.

To check the final collection:

```bash
python3 scripts/web18.py status
```

To reproduce the preliminary security scan:

```bash
semgrep scan --config=p/security-audit --metrics=off \
  --json \
  --output=data/processed/final-web-v1/semgrep_final.json \
  data/source/final-web-v1/
```

The original source files and scan outputs are retained for inspection. Automated findings and manual CWE assessments are treated as separate measurements.