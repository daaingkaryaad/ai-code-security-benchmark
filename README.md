# AI-generated code security benchmark

Team members: Ingkar Adilbek and Dinara Dyussembayeva  
Group: SE-2424  
Research Methods and Tools, Assignment 4

## Study

The final corpus contains 45 generated programs: 18 original outputs and 27 additional task-language outputs. Python, Java and JavaScript each contribute 15 programs. Nine pilot programs are separate. Each final task-language pair has one saved generation.

The frozen Semgrep scan reports zero alerts and zero scan errors across all 45 final sources. Calibration covers 24 authored controls: one of 12 positives was detected, 11 were missed, and all 12 negatives produced no target alert. These control outcomes describe this fixture set and configuration.

The single assessment matrix contains 180 complete program-CWE decisions: 60 applicable negative decisions and 120 non-applicable decisions. The supplementary functional audit passed 96 of 98 checks on the original Python and JavaScript programs. Two failed input cases concern one line-ending defect. That audit does not execute Java or the extension programs.

## Evidence index

| Location | Contents |
|---|---|
| `assessment/a4_review_consensus.csv` | Complete combined source assessment |
| `data/source/` | Original, extension and pilot source code |
| `data/raw/` | Saved response records |
| `data/processed/` | Raw scans, frozen rules, preparation records and analysis |
| `evidence/a4/` | Five figures derived from recorded study data |
| `evidence/literature/ssrn-6968361.pdf` | Full Aydın and Bahtiyar preprint |
| `fixtures/` | Synthetic database and 24 labelled controls |
| `logs/` | Collection events and recorded scanner version |
| `prompts/` | Final and pilot task prompts |
| `protocol/` | Task definitions, schedules, manifests, definitions, expectations and literature register |
| `scripts/` | Scanner, functional-audit and plotting implementations |

The complete run register is `data/processed/a4-analysis/a4_sample_results_45.csv`. The combined raw scans and frozen configuration are in `data/processed/a4-calibration-20261030T103600927206Z/`. Original expectations are preserved in `protocol/a3_expected_results_verbatim.txt`.