# Stage 2 – UK Study / UK Setting

## Updated Inclusion Rule
- Study is conducted in the **UK**, OR  
- Applied to a **UK setting** (including NHS, England, Wales, Scotland, Northern Ireland).
- If the setting is unclear/unstated, include but flag for Stage 8 manual review.

---

## Confusion Matrix

|                | Freddie Include | Freddie Exclude |
|----------------|-----------------|-----------------|
| **API Include** | 38             | 7              |
| **API Exclude** | 0              | 5             |

---

## Performance Metrics
- **True Positives (TP):** 38 
- **True Negatives (TN):** 5  
- **False Positives (FP):** 7  
- **False Negatives (FN):** 0  
- **Accuracy:** 86%  
- **Precision:** 84.4%  

---

## Changes vs previous run
- ✅ Removed all 14 prior false negatives by allowing Unknown setting → include & flag.  
- ⚠️ Introduced 7 false positives, each flagged for Stage 8 (expected with the new rule).
- Flagged FP IDs: J507, J510, J526, J538, J539, J548, J550
- Pattern: mostly Cochrane/systematic reviews with no explicit UK population/setting in the abstract.

- 

