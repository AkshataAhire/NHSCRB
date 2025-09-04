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

## Investigating false negatives
- Missed clinical contexts – Many exclusions were in clear healthcare settings (antenatal, hospitals, prescribing, physio, surgery).
- Too dependent on “UK/NHS” signals – Trials without explicit UK wording slipped through.
- Public health vs clinical – Lifestyle/exercise studies delivered in clinical or supervised settings were wrongly excluded.
- Systematic reviews – Cochrane reviews on treatments were misread as generic.
- Policy/health economics – PRIMEtime CE excluded despite being NHS/social care–focused.

## Action 
– Refine rule: include all studies in clinical, hospital, NHS, or policy settings, even if not labelled “UK.” Exclude only if purely lab-based or non-healthcare.
- Grey area: depends how strictly “health setting context” is interpreted.  

