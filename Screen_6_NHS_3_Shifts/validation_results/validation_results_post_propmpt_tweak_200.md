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
- **True Positives (TP):** 34  
- **True Negatives (TN):** 46  
- **False Positives (FP):** 11  
- **False Negatives (FN):**  12 

- **Accuracy:** 77.6%  
- **Precision:** 73.9%  

---

## Notes
- 12 false negatives identified.  
- 11 false positive
Next steps:
- Validate against full 361 articles
