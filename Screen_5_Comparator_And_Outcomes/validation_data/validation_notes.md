# Stage 5 – Comparator and outcomes

A) Uses a comparison group (e.g., business-as-usual/usual care/standard care, no intervention, do nothing, no change, control, comparator, placebo), AND
B) Measures primary outcomes related to cost or impact (e.g., cost reductions, costs/QALYs, change in outcome, change in impact, effectiveness, utilization/throughput, time, safety, clinical outcomes, patient-reported outcomes).

## Confusion Matrix

|                | Freddie Include | Freddie Exclude |
|----------------|-----------------|-----------------|
| **API Include** | 10              | 8               |
| **API Exclude** | 3               | 9               |

---

## Performance Metrics
- **True Positives (TP):** 10  
- **True Negatives (TN):** 9  
- **False Positives (FP):** 8  
- **False Negatives (FN):** 3  

- **Accuracy:** 60%  
- **Precision:** 75%  

---

## Notes
- 3 false negatives identified.  
- 9 false positives indicate possible over-inclusion by the API relative to Freddie.

- The FPs all had clear comparators and clinical/impact outcomes (e.g. mortality, morbidity, function, hospitalisation).
- We had 3 false negatives – all were marked as lacking a comparator by the API, but Freddie included them.
J515, J536, J549
- API struggled with less explicit framing.

- After discussing the false positives and whether Stage 5 be applied narrowly (e.g. only economics/cost outcomes), or broadly (clinical + impact + cost)?
- Freddie adding an extra column where I'm screening by the wider impacts/outcomes, which can replace my original stage 5 column
