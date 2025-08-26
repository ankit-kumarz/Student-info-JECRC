# Student Info Portal — OTP Auth + PDF
This project lets a student enter Roll No + Mobile, receive an OTP, verify, then **view all columns** from the Excel and **download PDF/CSV/JSON** of their own record.

## Structure
- `backend/` — Flask API (OTP, tokens, Excel read, PDF export)
- `frontend/` — Single HTML (Tailwind). Calls backend via fetch.
- `.gitignore` - Specifies intentionally untracked files that Git should ignore.

## Run
1) Backend
```
cd backend
python -m venv .venv
.\.venv\Scripts\activate             # Windows
# or: source .venv/bin/activate      # macOS/Linux
pip install -r requirements.txt

# Windows PowerShell
setx DATA_FILE "student_data.xlsx"
setx SHEET_NAME "Master Data 2022-26 Batch"
setx SECRET_KEY "your-long-random-secret"
setx DEBUG_OTP "true"
python app.py

# macOS/Linux
export DATA_FILE="student_data.xlsx"
export SHEET_NAME="Master Data 2022-26 Batch"
export SECRET_KEY="your-long-random-secret"
export DEBUG_OTP=true
python app.py
```

2) Frontend
- Open `frontend/index.html` in your browser.

> Put your Excel file in `backend/` as `student_data.xlsx` (or set `DATA_FILE`).

## SMS
- In production, integrate an SMS provider inside `/api/request-otp` where noted.
