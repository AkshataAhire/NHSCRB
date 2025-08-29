# Stage 1 Screening – English (2019–2025)

Automated **first-stage literature screening** using GPT.  
Inclusion criteria:  
1. Article is written in **English**  
2. Article published **between 2019 and 2025** (inclusive)

---

## Workflow diagram
<img width="1731" height="714" alt="image" src="https://github.com/user-attachments/assets/0ac08b56-3654-4338-9c59-bd5d95912e23" />


## File Descriptions

| File / Folder        | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `data/`              | Contains input/output CSVs (ignored in `.gitignore` except small samples). |
| `sample_articles.csv`| Example input file with `Unique_ID`, `Year`, `Title`, `Abstract`.           |
| `main_1.py`          | Main entry point. Loads data, runs pipeline, writes output.                 |
| `utils_1.py`         | Utility functions: prompt building, JSON parsing, result normalization.     |
| `openai_client.py`   | Wrapper for OpenAI client and API calls with retry logic.                   |
| `system_prompt_1.txt`| System prompt file that defines inclusion criteria and output schema.        |
| `README.md`          | Documentation for this stage.                                               |

---

## Workflow

1. **Input** → `sample_articles.csv`  
   Columns: `Unique_ID`, `Year`, `Title`, `Abstract`

2. **Process**  
   - `main_1.py` loops rows  
   - `utils_1.py` builds the user prompt  
   - `openai_client.py` sends prompt → GPT  
   - GPT returns strict JSON → parsed/normalized  
   - Results merged back to dataframe

3. **Output** → `screen_stage1.csv`  
   Original + new fields:
   - `include_stage1`
   - `reason_stage1`
   - `detected_language`
   - `publication_year`
   - `confidence_stage1`

---

## Usage

### 1. Activate environment
cd "C:\Users\NM2.TP5IJ4AX\OneDrive - NHS\Documents\Projects\NHSCRB\screen_1_2019_2025_English"
python -m venv .venv
.\.venv\Scripts\activate.bat
### 2. Set OpenAI API key
$env:OPENAI_API_KEY="sk-REPLACE_ME"
### 3. Run
python main_1.py --input data\sample_articles.csv --output data\screen_stage1.csv --sleep 0.3

### Optional flags:
--limit 5 → process only first 5 rows
--model gpt-4o → choose model
--system system_prompt_1.txt → custom system prompt
--sleep 0.5 → add delay between calls

## Example

### Input:
Unique_ID,Year,Title,Abstract
123,2021,"AI in Healthcare","This study explores..."

### GPT JSON output:
{
  "include": true,
  "reason": "English article from 2021",
  "detected_language": "English",
  "publication_year": 2021,
  "confidence": 0.92
}

### Output row:
123,2021,"AI in Healthcare","This study explores...",True,"English article from 2021",English,2021,0.92
pip install -r ..\requirements.txt
