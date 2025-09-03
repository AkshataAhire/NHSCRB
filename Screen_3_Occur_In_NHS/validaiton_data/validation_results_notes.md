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
| **API Include** | 23              | 0               |
| **API Exclude** | 1               | 0               |

---

## Performance Metrics
- **True Positives (TP):** 23  
- **True Negatives (TN):** 0  
- **False Positives (FP):** 0  
- **False Negatives (FN):** 1  

- **Accuracy:** 95.8%  
- **Precision:** 95.8%  

---

## Notes
- ❌ 1 false negative → **J525**  
  - API reason → *“Study uses cohort data without specific health setting context.”*  
  - Freddie reason → *“Bit unclear from abstract, but think it would be community/health setting.”*  
- Grey area: depends how strictly “health setting context” is interpreted.  

