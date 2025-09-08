# Stage 4 – Publication Type (Peer-reviewed vs Grey Literature)

## Inclusion Rule
- ✅ Include if peer-reviewed article OR grey literature (e.g., reports, dissertations, conference abstracts).  
- ❌ Exclude if study protocol, editorial/commentary, or predatory/non-peer-reviewed journal. 
- ⚠️ If publication type unknown/unclear → Include but flag for Stage 8 review (new tweak).

---

## Confusion Matrix

|                | Freddie Include | Freddie Exclude |
|----------------|-----------------|-----------------|
| **API Include** | 133              | 0               |
| **API Exclude** | 7               | 13               |

---

## Performance Metrics
- **True Positives (TP):** 133  
- **True Negatives (TN):** 13  
- **False Positives (FP):** 0  
- **False Negatives (FN):** 7  

- **Accuracy:** 95.4%  
- **Precision:** 95%  

---

## Notes
✅ Big improvement in recall: FN down 31 → 7 after “include-if-unknown” tweak.

✅ Still 0 FP — continues to reliably exclude protocols/editorials.

🔎 7 FN remain (API excluded but Freddie included). Action: send these 7 IDs to Freddie for review/confirmation of publication type.
