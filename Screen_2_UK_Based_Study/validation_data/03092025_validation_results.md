# Stage 2 – UK Study / UK Setting

## Inclusion Rule
- Study is conducted in the **UK**, OR  
- Applied to a **UK setting** (including NHS, England, Wales, Scotland, Northern Ireland).
- Where there is no explicit setting provided, UK or not UK, the articles is included but flagged for Review in manual screening stage 8 (if it gets that far) 

---

## Confusion Matrix

|                | Freddie Include | Freddie Exclude |
|----------------|-----------------|-----------------|
| **API Include** | 24              | 0               |
| **API Exclude** | 14              | 12              |

---

## Performance Metrics
- **True Positives (TP):** 24  
- **True Negatives (TN):** 12  
- **False Positives (FP):** 0  
- **False Negatives (FN):** 14  
- **Accuracy:** 72%  
- **Precision:** 63.2%  

---

## Notes
- ✅ No false positives → API was conservative (didn’t wrongly include non-UK studies).  
- ❌ 14 false negatives → API failed to recognise genuine UK-based studies.  
- Error pattern → the model seems to only pick up **explicit UK mentions** (e.g. “NHS”, “England”), and under-detects more **implicit indicators**.  
- Next step → review the 14 false negatives with Freddie to agree what subtler indicators should count as UK setting.  

I’ve gone through the Stage 2 false negatives and noticed a clear pattern: all of them are Cochrane systematic reviews. None of the abstracts explicitly mention UK populations, NHS settings, or UK-specific registries. The only UK link is that the Cochrane review groups themselves are headquartered in the UK.
 
So the key question for us is: do we treat UK-based organisations (like Cochrane, NICE, etc.) as sufficient for “UK setting,” or do we only include when the participants/data are explicitly UK-based?
