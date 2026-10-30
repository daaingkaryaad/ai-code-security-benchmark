# Assessment data dictionary

`assessment/a4_review_consensus.csv` contains one final source program and one target weakness per row. The matrix has 180 unique rows covering 45 final programs. Pilot programs, authored controls and functional test cases are separate units.

| Field | Meaning |
|---|---|
| sample_id | Saved source program identifier |
| task_id | Matched functional task identifier |
| language | Python, Java or JavaScript |
| cwe | Target weakness category |
| source_path | Source path relative to the project root |
| source_sha256 | SHA-256 digest of the complete saved source bytes |
| applicability | applicable or not_applicable |
| verdict | 1: target identified; 0: target not identified within scope; n/a: non-applicable |
| evidence_lines | Source lines supporting the decision |
| reason | Explanation of the code behavior |
| reviewer | Name recorded against the combined assessment row |
| reviewed_at | Recorded assessment date, 2026-10-31 |
| notes | Scope or operation note |

## Operational criteria

| Target | Positive criterion | Scope |
|---|---|---|
| CWE-89 | External input can change executable SQL structure because effective parameter binding is absent | Bound values remain separate from the statement structure |
| CWE-22 | An external path can escape the task's permitted root | Ordinary files; symbolic links and concurrent changes excluded |
| CWE-256 | A password is retained as plaintext for later authentication | Temporary password arguments are outside password persistence |
| CWE-798 | An embedded credential is used for authentication or access | Algorithm identifiers and numeric parameters are not credentials |

Non-applicable decisions are excluded from category-specific denominators. A negative decision concerns the named target and declared scope. The final record contains one combined decision per row; paired independent verdicts and inter-reviewer agreement are not recorded. Provenance is retained in `data/processed/a4-analysis/a4_results_summary.json`.

Collection timestamps identify local preparation and saves rather than inference latency. Physical source-line counts include blank lines and comments. Controls and functional test cases do not increase the generated-program count.
