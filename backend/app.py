from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
import pandas as pd
import os, re, time, random, io
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from twilio.rest import Client  # Add this import

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ====== Config ======
DATA_FILE = os.environ.get("DATA_FILE", "student_data.xlsx")
SHEET_NAME = os.environ.get("SHEET_NAME")  # if None, use first sheet
SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret")
OTP_TTL_SECONDS = int(os.environ.get("OTP_TTL_SECONDS", "300"))       # 5 minutes
TOKEN_TTL_SECONDS = int(os.environ.get("TOKEN_TTL_SECONDS", "1800"))  # 30 minutes
DEBUG_OTP = os.environ.get("DEBUG_OTP", "true").lower() == "true"     # return OTP in response for local testing

# Twilio configuration
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

# Initialize Twilio client if credentials are available
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
else:
    twilio_client = None
    print("Twilio credentials not found. SMS sending will be disabled.")

serializer = URLSafeTimedSerializer(SECRET_KEY)

# In-memory OTP store
# key = f"{roll.lower()}::{last10(mobile)}" -> {"otp": "123456", "exp": epoch_seconds, "attempts": 0}
OTP_STORE = {}

# Cache dataframe
DF = None

# ====== Helpers ======
def normalize_col(name: str) -> str:
    return re.sub(r'\s+', ' ', str(name)).strip()

def load_dataframe():
    global DF
    if DF is not None:
        return DF
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Excel file not found: {DATA_FILE}. Put your Excel in backend/ as '{DATA_FILE}' or set DATA_FILE env var.")
    if SHEET_NAME:
        df = pd.read_excel(DATA_FILE, sheet_name=SHEET_NAME)
    else:
        xls = pd.ExcelFile(DATA_FILE)
        df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    df.columns = [normalize_col(c) for c in df.columns]
    DF = df
    return DF

def find_roll_col(columns):
    patterns = [
        r'^(university\s*)?roll\s*no\.?$',
        r'^(roll\s*no\.?|roll\s*number)$',
        r'^\s*university\s*roll\s*no\.?\s*$',
        r'^\s*enrollment\s*no\.?\s*$'
    ]
    for c in columns:
        for p in patterns:
            if re.match(p, c, re.I):
                return c
    for c in columns:
        if 'roll' in c.lower():
            return c
    return None

def find_mobile_cols(columns):
    out = []
    for c in columns:
        lc = c.lower()
        if any(k in lc for k in ["mobile", "phone", "contact", "whatsapp"]):
            out.append(c)
    return out

def digits_only(s):
    return re.sub(r'\D+', '', str(s))

def make_key(roll: str, mobile: str):
    md = digits_only(mobile)
    md = md[-10:] if len(md) >= 10 else md[-8:]  # last 8-10 digits
    return f"{roll.strip().lower()}::{md}"

def sign_token(roll: str):
    return serializer.dumps({"roll": roll})

def verify_token(token: str):
    try:
        data = serializer.loads(token, max_age=TOKEN_TTL_SECONDS)
        return data.get("roll")
    except (BadSignature, SignatureExpired):
        return None

def get_student_row(roll: str):
    df = load_dataframe()
    rcol = find_roll_col(df.columns)
    if not rcol:
        return None, "Roll number column not found in Excel."
    mask = df[rcol].astype(str).str.strip().str.lower() == roll.strip().lower()
    if not mask.any():
        return None, f"No record found for roll '{roll}'."
    row = df[mask].iloc[0]
    return row, None

def send_pdf_from_row(row: pd.Series, title="Student Record"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x_left = 2*cm
    y = height - 2*cm

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x_left, y, title)
    y -= 1*cm

    c.setFont("Helvetica", 10)
    for col, val in row.items():
        text = f"{col}: {'' if pd.isna(val) else str(val)}"
        # Wrap long lines
        max_chars = 95
        while len(text) > max_chars:
            c.drawString(x_left, y, text[:max_chars])
            y -= 0.6*cm
            text = "    " + text[max_chars:]
            if y < 2*cm:
                c.showPage()
                y = height - 2*cm
                c.setFont("Helvetica", 10)
        c.drawString(x_left, y, text)
        y -= 0.6*cm
        if y < 2*cm:
            c.showPage()
            y = height - 2*cm
            c.setFont("Helvetica", 10)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ====== Routes ======
@app.route("/api/health")
def health():
    try:
        df = load_dataframe()
        return jsonify({"status": "ok", "rows": int(df.shape[0]), "cols": int(df.shape[1])})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/request-otp", methods=["POST"])
def request_otp():
    data = request.get_json(force=True, silent=True) or {}
    roll = str(data.get("roll", "")).strip()
    mobile = str(data.get("mobile", "")).strip()
    country_code = str(data.get("country_code", "+91")).strip()  # Default to +91 (India)
    if not roll or not mobile:
        return jsonify({"error": "roll and mobile are required"}), 400

    df = load_dataframe()
    rcol = find_roll_col(df.columns)
    mcols = find_mobile_cols(df.columns)
    if not rcol:
        return jsonify({"error": "Could not detect Roll No column in Excel"}), 500
    if not mcols:
        return jsonify({"error": "Could not detect any Mobile/Phone column in Excel"}), 500

    mask_roll = df[rcol].astype(str).str.strip().str.lower() == roll.lower()
    if not mask_roll.any():
        return jsonify({"error": f"No record found for roll '{roll}'"}), 404

    # Check mobile matches at least by suffix (last 8-10 digits) in any mobile-like column
    row = df[mask_roll].iloc[0]
    mobile_digits = digits_only(mobile)
    if len(mobile_digits) < 8:
        return jsonify({"error": "Mobile number seems too short"}), 400

    def row_has_mobile_suffix(row):
        for c in mcols:
            val = digits_only(row.get(c, ""))
            if not val:
                continue
            for n in (10, 9, 8):
                if len(mobile_digits) >= n and len(val) >= n and mobile_digits[-n:] == val[-n:]:
                    return True
        return False

    if not row_has_mobile_suffix(row):
        return jsonify({"error": "Mobile number does not match our records"}), 403

    # Generate and store OTP
    otp = f"{random.randint(100000, 999999)}"
    key = make_key(roll, mobile)
    OTP_STORE[key] = {"otp": otp, "exp": time.time() + OTP_TTL_SECONDS, "attempts": 0}

    # Send SMS via Twilio if configured
    if twilio_client:
        try:
            # Format mobile number with country code
            formatted_mobile = f"{country_code}{mobile}"

            message = twilio_client.messages.create(
                body=f"Your OTP for student login is: {otp}. It will expire in 5 minutes.",
                from_=TWILIO_PHONE_NUMBER,
                to=formatted_mobile
            )
            print(f"SMS sent to {formatted_mobile}, SID: {message.sid}")
        except Exception as e:
            print(f"Failed to send SMS: {str(e)}")
            import traceback
            traceback.print_exc()
            # Don't fail the request, just log the error

    payload = {"message": "OTP sent successfully"}
    if DEBUG_OTP:
        payload["dev_otp"] = otp  # for local testing

    return jsonify(payload), 200

@app.route("/api/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json(force=True, silent=True) or {}
    roll = str(data.get("roll", "")).strip()
    mobile = str(data.get("mobile", "")).strip()
    otp = str(data.get("otp", "")).strip()

    if not roll or not mobile or not otp:
        return jsonify({"error": "roll, mobile and otp are required"}), 400

    key = make_key(roll, mobile)
    entry = OTP_STORE.get(key)
    if not entry:
        return jsonify({"error": "OTP not requested or expired"}), 400

    if time.time() > entry["exp"]:
        OTP_STORE.pop(key, None)
        return jsonify({"error": "OTP expired"}), 400

    entry["attempts"] += 1
    if entry["otp"] != otp:
        if entry["attempts"] >= 5:
            OTP_STORE.pop(key, None)
            return jsonify({"error": "Too many failed attempts"}), 403
        return jsonify({"error": "Invalid OTP"}), 401

    # Success -> issue token and clear OTP
    token = sign_token(roll)
    OTP_STORE.pop(key, None)
    return jsonify({"token": token}), 200

def extract_bearer(req):
    auth = req.headers.get("Authorization", "")
    if auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()
    return None

@app.route("/api/me", methods=["GET"])
def me():
    token = extract_bearer(request)
    if not token:
        return jsonify({"error": "Missing Bearer token"}), 401
    roll = verify_token(token)
    if not roll:
        return jsonify({"error": "Invalid or expired token"}), 401

    row, err = get_student_row(roll)
    if err:
        return jsonify({"error": err}), 404

    # Return all columns
    out = {}
    for k, v in row.items():
        if pd.isna(v):
            out[str(k)] = None
        else:
            out[str(k)] = v if isinstance(v, (str,)) else (float(v) if isinstance(v, (int, float)) else str(v))
    return jsonify({"roll": roll, "data": out}), 200

@app.route("/api/me/pdf", methods=["GET"])
def me_pdf():
    token = extract_bearer(request)
    if not token:
        return jsonify({"error": "Missing Bearer token"}), 401
    roll = verify_token(token)
    if not roll:
        return jsonify({"error": "Invalid or expired token"}), 401

    row, err = get_student_row(roll)
    if err:
        return jsonify({"error": err}), 404

    pdf = send_pdf_from_row(row, title=f"Student Record — {roll}")
    return send_file(pdf, mimetype="application/pdf", as_attachment=True, download_name=f"{roll}.pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
