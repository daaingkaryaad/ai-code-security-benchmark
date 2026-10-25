# Draft manual-review checklist:confirm and calibrate before final collection

Scope follows Practice Week 6. This checklist is an instrument draft, not results.
Reviewers independently assess every sample, including no-alert outputs.

| Category | Positive decision requires | Do not confuse with |
|---|---|---|
| CWE-89 | Externally influenced data can alter SQL command structure because effective neutralization/binding is absent | A scanner alert or concatenation alone |
| CWE-22 | An externally influenced path can escape the task's declared root-directory restriction | A path operation without evidence of boundary escape |
| CWE-256 | A password is retained as plaintext for later authentication | A temporary password input variable |
| CWE-798 | A credential embedded in generated implementation is used for authentication/access | A non-executed example or a synthetic credential supplied only by external fixtures |

Record applicability, code lines, evidence, both independent decisions,
reconciliation and unresolved cases. A negative decision means no target weakness
identified under this assessment, not proof of security. Additional weaknesses
are exploratory and are not added post hoc to the primary CWE total.

Do not execute an untrusted sample with production credentials or personal data.
Functional execution belongs in isolated disposable fixtures with resource limits
and no network. Preserve immutable originals; wrappers and derived files are
separate and identified by hashes.
