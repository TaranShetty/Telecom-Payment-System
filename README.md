# Telecom AI Payment System

## Overview
The **Telecom AI Payment System** is a web-based enterprise application developed to streamline telecom payment management and tracking. The system provides a centralized platform for submitting, monitoring, and analyzing telecom payment requests along with vendor and service-wise records. It also includes an AI-assisted chatbot to support users with navigation and operational queries.

This project focuses on automation, data consistency, and usability, making it suitable for internal organizational use and academic evaluation.

---

## Features
- Secure user authentication (Login and Registration)
- Telecom payment request submission
- Centralized dashboard for payment tracking
- Service-wise modules (MPLS and Bandwidth)
- Vendor and commission management
- Persistent data storage using SQLite
- AI-assisted chatbot for user guidance
- Responsive user interface using Bootstrap
- Structured CRUD operations for telecom records

---

## Technology Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
- **Database:** SQLite
- **Data Handling:** pandas
- **Authentication:** Session-based authentication using Flask
- **AI Component:** Rule-based chatbot logic
- **Utilities:** sqlite3, re, os, pathlib

---

## Project Structure

```telecom-ai-payment-system/
│
├── test_app.py                 # Main Flask application
├── chatbot_logic.py            # Backend chatbot logic
├── database.py                 # Database helper functions
├── db.py                       # SQLite database operations
├── requirements.txt            # Project dependencies
│
├── telecom.db                  # SQLite database for telecom payment data
├── users.db                    # SQLite database for user authentication
│
├── templates/                  # HTML templates
│   ├── base.html
│   ├── base_focus.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── request_payment.html
│   ├── chatbot.html
│   ├── info.html
│   ├── mpls.html
│   ├── mpls_vendor.html
│   ├── bandwidth_vendor.html
│   ├── airtel_commission.html
│   └── new_commission.html
│
├── static/
│   ├── css/
│   │   └── style.css           # Custom styling
│   │
│   ├── js/
│   │   └── chatbot.js          # Frontend chatbot script
│   │
│   └── data/
│       ├── Payment ALL Updated.xlsx
│       └── Payment ALL Updated (2).xlsx
│
├── __pycache__/                # Python cache files
│
└── README.md```

