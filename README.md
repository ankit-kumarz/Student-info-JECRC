# 🎓 Student Information Portal

A **modern full-stack web application** for managing and viewing student academic & personal information with a **secure OTP-based authentication system**.

---

## 📋 Overview

The **Student Information Portal** provides students with a centralized platform to securely access their **profiles, educational details, and academic records**.
It comes with a **responsive dashboard**, **OTP login**, and support for **data export** in multiple formats.

---

## ✨ Features

* 🔑 **Secure Authentication** – OTP-based login via mobile verification
* 📊 **Student Dashboard** – Clean, modern UI with collapsible sections
* 📝 **Comprehensive Student Data**:

  * Personal information
  * 10th and 12th grade details
  * Undergraduate academic records
  * Semester-wise GPA tracking
* 📤 **Data Export** – Download data in **JSON, CSV, and PDF** formats
* 📱 **Responsive Design** – Works seamlessly on desktop and mobile
* 🚪 **Logout Functionality** – Secure session management

---

## 🏗️ Project Structure

```
Student Info Portal/
├── backend/
│   ├── app.py              # Flask backend API
│   ├── requirements.txt    # Python dependencies
│   ├── student_data.xlsx   # Student database (Excel)
│   └── README.md           # Backend documentation
├── frontend/
│   ├── index.html          # Main frontend application
│   ├── server.py           # Optional development server
│   └── README.md           # Frontend documentation
```

---

## 🚀 Installation & Setup

### ✅ Prerequisites

* Python **3.7+**
* Flask
* Pandas
* A modern web browser

### 🔹 Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

* Place your Excel file (`student_data.xlsx`) in the backend directory.
* Ensure it contains **roll numbers, mobile numbers, and academic records**.
* Run the Flask server:

```bash
python app.py
```

Backend runs at: **[http://localhost:5000](http://localhost:5000)**

---

### 🔹 Frontend Setup

```bash
cd frontend
python server.py
```

Or with Python’s built-in server:

```bash
python -m http.server 5500
```

Frontend runs at: **[http://localhost:5500](http://localhost:5500)**

---

## 🔧 Configuration

### 🌍 Environment Variables (Optional)

```bash
DATA_FILE="student_data.xlsx"    # Path to Excel file
SHEET_NAME="Sheet1"              # Excel sheet name
SECRET_KEY="your-secret-key"     # Token generation secret
OTP_TTL_SECONDS="300"            # OTP validity (5 min)
TOKEN_TTL_SECONDS="1800"         # Token validity (30 min)
DEBUG_OTP="true"                 # Show OTP in response (testing only)
```

### 📑 Excel File Format

Your Excel file should include these columns:

* **University Roll No.**
* **Contact No.** (mobile number)
* **Student Name, Father’s Name, Section, Gender, DOB**
* **University Email, Present Address**
* **10th & 12th Board, Percentage/Grades**
* **Branch, Specialization, CGPA**
* **Semester-wise GPA (I, II, III, …)**

---

## 🎯 Usage

1. **Login** – Enter roll number & mobile number to receive OTP
2. **Verify** – Enter OTP to log in
3. **Dashboard** – View personal & academic data
4. **Navigate** – Expand/collapse sections
5. **Export** – Download data as **JSON, CSV, or PDF**
6. **Logout** – End session securely

---

## 🔌 API Endpoints

| Method | Endpoint           | Description                                  |
| ------ | ------------------ | -------------------------------------------- |
| POST   | `/api/request-otp` | Request OTP for authentication               |
| POST   | `/api/verify-otp`  | Verify OTP & get token                       |
| GET    | `/api/me`          | Fetch student data (auth required)           |
| GET    | `/api/me/pdf`      | Download student data as PDF (auth required) |
| GET    | `/api/health`      | Health check                                 |

---

## 🛠️ Technology Stack

### 🌐 Frontend

* HTML5, CSS3, JavaScript (ES6+)
* Tailwind CSS for styling
* FontAwesome icons
* Responsive design

### ⚙️ Backend

* Python **Flask** web framework
* **Pandas** for Excel processing
* **itsdangerous** for token authentication
* CORS support for cross-origin requests

---

## 🔒 Security Features

* OTP-based mobile verification
* Token-based authentication with expiry
* CORS configuration for secure requests
* Input validation & error handling
* Secure storage using `localStorage`

---

## 📱 Browser Support

* Chrome ✅ (recommended)
* Firefox
* Safari
* Edge
* Mobile browsers (iOS Safari, Chrome Mobile)

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch → `git checkout -b feature/amazing-feature`
3. Commit changes → `git commit -m 'Add amazing feature'`
4. Push branch → `git push origin feature/amazing-feature`
5. Open a Pull Request 🚀

---

## 📄 License

This project is for **educational purposes** only.
⚠️ Ensure compliance with your institution’s **data privacy policies** before deploying.

---

## 🆘 Troubleshooting

### Common Issues

* **CORS Errors** – Check frontend & backend ports
* **Excel File Not Found** – Ensure file path is correct
* **OTP Issues** – Verify mobile format matches input
* **Token Errors** – Clear browser `localStorage`

### Debugging Checklist

* Backend health check → [http://localhost:5000/api/health](http://localhost:5000/api/health)
* Frontend running at → [http://localhost:5500](http://localhost:5500)
* Verify Excel columns & names
* Open **browser console** for JS errors

---

## 🙏 Acknowledgments

* Built with **Flask** & **Tailwind CSS**
* Icons from **FontAwesome**
* OTP authentication design for secure access

---

👉 This portal is designed to help **educational institutions** provide students with **secure access to academic records** while ensuring compliance with **data protection regulations**.

