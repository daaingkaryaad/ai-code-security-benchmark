# calibration controls

24 authored source controls cover four target cwe categories, three languages and positive/negative labels. labels, reasons, provenance and source hashes are recorded in manifest.csv. these controls are excluded from generated-program frequencies.

the recorded combined scan is in data/processed/a4-calibration-20261030T103600927206Z. it detected one of twelve positives, missed eleven, and produced no target alert on the twelve negative examples. these results describe this small control set and frozen instrument rather than general scanner accuracy.

positive means the named weakness is present under the declared scope. negative means that target weakness is absent under that scope, without certifying complete security. file fixtures exclude symbolic links and concurrent filesystem changes. credentials used in positive controls are synthetic. static scanning does not require executing java.

retain the declared labels when a scanner misses a case. expanded rules constitute a separately documented instrument and require rerunning every control and all final sources. no fixture source bytes or labels were changed during project cleanup.
