# Stage 1 – English + 2019–2025

## Inclusion Rule
- Article must be written in **English**  
- Published between **2019–01–01 and 2025–12–31 (inclusive)**  

---

## Confusion Matrix

|                | Freddie Include | Freddie Exclude |
|----------------|-----------------|-----------------|
| **API Include** | 50              | 0               |
| **API Exclude** | 1               | 0               |

---

## Performance Metrics
- **True Positives (TP):** 50  
- **True Negatives (TN):** 0  
- **False Positives (FP):** 0  
- **False Negatives (FN):** 1  
- **Accuracy:** 98.0%  
- **Precision:** 98.0%  

---

## Notes
- **J517** was a false negative:  
  - API reason → *“Copyright indicates publication in 2017”*  
  - Freddie reason → *“Date and language ok”*  
- The metadata year was 2019 → that’s why Freddie marked it *include*.  
- But the abstract itself clearly states:  
  - Studies included up to **2014**  
  - Costs adjusted to **2016 USD**  
  - **Copyright © 2017 Elsevier Ltd**  
- This strongly suggests the actual publication year is **2017**, not 2019.  
