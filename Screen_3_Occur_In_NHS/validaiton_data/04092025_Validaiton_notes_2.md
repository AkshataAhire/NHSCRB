# Stage 3 – Occurs in NHS / Health & Social Care / Community Health Settings

## Inclusion Rule
- Study occurs in:  
  - **NHS settings (any level)**, OR  
  - **Health & Social Care services**, OR  
  - **Community health settings** (e.g., hospitals, primary care/GP, outpatient/ambulatory clinics, community clinics, patients' homes).  

---

## Confusion Matrix

|                | Freddie Include | Freddie Exclude |
|----------------|-----------------|-----------------|
| **API Include** | 36              | 0               |
| **API Exclude** | 5              | 4               |

---

## Performance Metrics
- **True Positives (TP):** 36
- **True Negatives (TN):** 4  
- **False Positives (FP):** 0  
- **False Negatives (FN):** 5  

- **Accuracy:** 88.9%  
- **Precision:** 87.8%  

---

## Notes
- ❌ 5 false negatives → down from 16. All edge cases where setting is implied but not clearly stated.
– Current rule is much stronger: fewer misses, no false positives.
