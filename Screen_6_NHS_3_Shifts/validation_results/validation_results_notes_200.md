# Stage 6 – NHS “Three Shifts” (Hospital→Community, Analogue→Digital, Sickness→Prevention)

Inclusion Rule (as tested)
INCLUDE only if the article explicitly relates to ≥1 of:
1. Hospital → Community (moving care out of hospital into community services)
2. Analogue → Digital (digital replacing analogue/admin-heavy processes)
3. Sickness → Prevention (proactive, predictive, preventive models)
EXCLUDE if none apply or evidence is unclear/ambiguous.

## Confusion Matrix

|                | Freddie Include | Freddie Exclude |
|----------------|-----------------|-----------------|
| **API Include** | 18              | 8               |
| **API Exclude** | 22              | 45               |

---

## Performance Metrics
- **True Positives (TP):** 18  
- **True Negatives (TN):** 45  
- **False Positives (FP):** 22  
- **False Negatives (FN):**  8 

- **Accuracy:** 67.7%  
- **Precision:** 45%  

---

## Notes
- 8 false negatives identified.  
- 22 false positive
Next steps:

Improve recognition of implicit shift framing (e.g., “earlier discharge” → hospital→community, “risk stratification” → prevention).

Decide whether to leave Stage 6 broad and rely on Stage 8 manual review to refine.
