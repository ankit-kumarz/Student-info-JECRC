# Backend (Flask) — OTP + PDF
## Setup
1) Put your Excel file in this folder and rename to `student_data.xlsx`
   - Or set env var `DATA_FILE` to your Excel filename.
   - If needed, set `SHEET_NAME` (e.g., `Master Data 2022-26 Batch`).
2) Create venv and install dependencies:
```
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```
3) Run:
```
# Windows PowerShell
setx DATA_FILE "student_data.xlsx"
setx SHEET_NAME "Master Data 2022-26 Batch"
setx SECRET_KEY "your-long-random-secret"
setx DEBUG_OTP "true"
python app.py
```
```
# macOS/Linux (same folder)
export DATA_FILE="student_data.xlsx"
export SHEET_NAME="Master Data 2022-26 Batch"
export SECRET_KEY="your-long-random-secret"
export DEBUG_OTP=true
python app.py
```

## API
- `POST /api/request-otp`  JSON: `{ "roll": "...", "mobile": "..." }`
- `POST /api/verify-otp`   JSON: `{ "roll": "...", "mobile": "...", "otp": "123456" }` -> `{ "token": "<bearer>" }`
- `GET  /api/me`           Headers: `Authorization: Bearer <token>` -> returns **all columns** for that student
- `GET  /api/me/pdf`       Headers: `Authorization: Bearer <token>` -> returns a **PDF** of the student's record

> For production, integrate an SMS provider in `/api/request-otp` where marked.
