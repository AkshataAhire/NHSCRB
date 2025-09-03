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
| **API Include** | 25              | 0               |
| **API Exclude** | 16              | 4               |

---

## Performance Metrics
- **True Positives (TP):** 25
- **True Negatives (TN):** 4  
- **False Positives (FP):** 0  
- **False Negatives (FN):** 16  

- **Accuracy:** 64.4%  
- **Precision:** 60.9%  

---

## Notes
- ❌ 16 false negatives → 14 look to be "stage 2 flagged for review"
- Need to investigate.
- Grey area: depends how strictly “health setting context” is interpreted.  

