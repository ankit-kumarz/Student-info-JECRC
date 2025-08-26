Student Information Portal
A modern web application for managing and viewing student information with a secure authentication system.

📋 Overview
The Student Information Portal is a full-stack web application that allows students to securely access their academic and personal information through an OTP-based authentication system. It features a clean, responsive dashboard that displays student profiles, educational details, and academic records.

✨ Features
Secure Authentication: OTP-based login system via mobile verification

Student Dashboard: Clean, modern UI with collapsible sections

Comprehensive Student Data:

Personal information

10th and 12th grade details

Undergraduate academic records

Semester-wise GPA tracking

Data Export: Download student data in JSON, CSV, and PDF formats

Responsive Design: Works seamlessly on desktop and mobile devices

Logout Functionality: Secure session management

🏗️ Project Structure
text
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
🚀 Installation & Setup
Prerequisites
Python 3.7+

Flask

Pandas

A modern web browser

Backend Setup
Navigate to backend directory:

bash
cd backend
Install dependencies:

bash
pip install -r requirements.txt
Prepare your data:

Place your Excel file with student data in the backend directory

Ensure the file contains columns for roll numbers, mobile numbers, and academic records

Run the Flask server:

bash
python app.py
The backend will start on http://localhost:5000

Frontend Setup
Navigate to frontend directory:

bash
cd frontend
Run the development server:

bash
python server.py
Or use Python's built-in server:

bash
python -m http.server 5500
Access the application:
Open your browser and navigate to http://localhost:5500

🔧 Configuration
Environment Variables (Optional)
The backend supports these environment variables:

bash
DATA_FILE="student_data.xlsx"           # Path to Excel file
SHEET_NAME="Sheet1"                     # Excel sheet name
SECRET_KEY="your-secret-key"            # For token generation
OTP_TTL_SECONDS="300"                   # OTP expiration time (5 minutes)
TOKEN_TTL_SECONDS="1800"                # Token expiration time (30 minutes)
DEBUG_OTP="true"                        # Show OTP in response for testing
Excel File Format
Your Excel file should include these columns (names can be customized):

University Roll No.

Contact No. (or similar mobile number field)

Name of the Student

Father's Name

Section

Gender

Date of Birth

University E-Mail ID

Present Address

10th Board, 10th Percentage, etc.

12th Board, 12th Percentage, etc.

Branch, Specialization, CGPA

Semester-wise GPA (I Sem GPA, II Sem GPA, etc.)

🎯 Usage
Login: Enter roll number and mobile number to receive OTP

Verification: Enter the OTP sent to your mobile device

Dashboard: View your complete academic profile

Navigation: Use collapsible sections to explore different information categories

Export: Download your data using the JSON, CSV, or PDF buttons

Logout: Use the logout button to end your session

🔌 API Endpoints
POST /api/request-otp - Request OTP for authentication

POST /api/verify-otp - Verify OTP and receive authentication token

GET /api/me - Get student data (requires authentication)

GET /api/me/pdf - Download student data as PDF (requires authentication)

GET /api/health - Health check endpoint

🛠️ Technology Stack
Frontend
HTML5, CSS3, JavaScript (ES6+)

Tailwind CSS for styling

FontAwesome icons

Modern responsive design

Backend
Python Flask web framework

Pandas for Excel data processing

JWT-like token authentication using itsdangerous

CORS support for cross-origin requests

🔒 Security Features
OTP-based mobile verification

Token-based authentication with expiration

CORS configuration for secure cross-origin requests

Input validation and error handling

Secure token storage in localStorage

📱 Browser Support
Chrome (recommended)

Firefox

Safari

Edge

Mobile browsers (iOS Safari, Chrome Mobile)

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📄 License
This project is for educational purposes. Please ensure compliance with your institution's data privacy policies when deploying.

🆘 Troubleshooting
Common Issues
CORS Errors: Ensure both frontend and backend are running on correct ports

Excel File Not Found: Check the file path in backend directory

OTP Not Working: Verify mobile number format in Excel file matches input

Token Errors: Clear browser localStorage if experiencing authentication issues

Getting Help
Check that both servers are running:

Backend: http://localhost:5000/api/health

Frontend: http://localhost:5500

Verify Excel file format matches expected column names

Check browser console for JavaScript errors

🙏 Acknowledgments
Built with Flask and Tailwind CSS

Icons provided by FontAwesome

OTP authentication pattern for secure access

Note: This application is designed for educational institutions to provide students with secure access to their academic records. Always ensure compliance with data protection regulations when handling student information.
