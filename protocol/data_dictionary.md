> these fields describe the existing **api collector**, not the manually collected chatgpt outputs. see `WEB_COLLECTION.md` for current web records.

# Collection records and review fields

`collection_inventory.csv` is derived from saved per-sample JSON records. Rebuild
it with `python scripts/study.py audit`; do not edit it as raw evidence.

| Field | Meaning |
|---|---|
| partition | pilot or final |
| batch | Versioned collection batch; pilot-v1 is distinct from pilot-v2 |
| sample_id | Task ID, language code and repetition; unique within a batch |
| task_id / domain | Locked specification and domain |
| language | PY, JAVA or JS |
| repetition | 1 for initial pilot, 1–3 for final |
| status | Collection outcome, not a security verdict |
| model | Returned API model identifier |
| response_status | Provider-reported completion status |
| extraction_status | Verbatim unvalidated, enclosing fence removed, manual extraction needed, or no text |
| source_path / source_sha256 | Path and digest of extracted source; not proof of syntax or correctness |
| duplicate_of | First matching source digest across recorded batches; duplicates remain |
| input_tokens / cached_input_tokens | Provider-reported input usage |
| output_tokens / reasoning_tokens | Output total and its reasoning subset; do not add the subset to the total again |
| estimated_cost_usd | Estimate from recorded usage and configured rates; blank means unknown, not free |
| timestamp_utc | Event timestamp; request start and HTTP attempt timestamps are stored separately |

Collection statuses include `response_received`, `refused`, `response_incomplete`,
`model_mismatch`, `no_text`, `api_error`, `transport_outcome_unknown`,
`interrupted_outcome_unknown` and `pending`. Preserve all recorded reasons.
`response_received` means a completed response with text from the chosen snapshot,
not that the answer is valid code or that security analysis succeeded.

The manual review has separate applicability, reviewer A, reviewer B, reconciled
verdict, code evidence, assessment status and functional status. Keep unknown and
unreviewed values blank/pending. Never use '0' as a missing-value code. Record
non-applicability separately and do not interpret it as evidence of superior
security. Apply the finalized counting conventions consistently.
