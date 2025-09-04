# Stage 4 – Publication Type (Peer-reviewed vs Grey Literature)

## Inclusion Rule
- ✅ Include if peer-reviewed article OR grey literature (e.g., reports, dissertations, conference abstracts).  
- ❌ Exclude if study protocol, editorial/commentary, or predatory/non-peer-reviewed journal.  

---

## Confusion Matrix

|                | Freddie Include | Freddie Exclude |
|----------------|-----------------|-----------------|
| **API Include** | 19              | 0               |
| **API Exclude** | 1               | 3               |

---

## Performance Metrics
- **True Positives (TP):** 19  
- **True Negatives (TN):** 3  
- **False Positives (FP):** 0  
- **False Negatives (FN):** 1  

- **Accuracy:** 95.7%  
- **Precision:** 95.0%  

---

## Notes
- ❌ 1 false negative → **J532**  
  - **API reason:** *“Appears to be an editorial/commentary on policy experiences.”*  
  - **API classification:** *Editorial/Commentary* (confidence 0.9) → excluded  
  - **Freddie screen:** *Include*  
  - **Freddie reason:** *Correct study type*  
- Disagreement likely arises from subjective judgement: API read it as commentary, Freddie treated it as valid study-type.  

---
