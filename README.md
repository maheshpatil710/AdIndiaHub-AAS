# AdIndiaHub – Advertisement Agency System

AdIndiaHub is a web-based Advertisement Agency Management System developed using Python Flask and MySQL.  
The system helps clients request marketing campaigns, while the admin creates and uploads advertisement videos and manages campaigns efficiently.

---

## 📌 Project Overview

Advertisement agencies manage multiple clients, campaigns, and marketing content manually, which is time-consuming and error-prone.  
This project automates the process of campaign requests, approval, advertisement video management, and campaign tracking.  

In this system:
- Clients can request marketing campaigns.
- Admin creates advertisement videos and assigns them to campaigns.
- Clients can only view videos (no upload permission).
- The system helps agencies manage marketing workflows digitally.

---

## 🎯 Objectives of the Project

- To develop an automated Advertisement Agency Management System.
- To reduce manual work in campaign handling.
- To provide a centralized platform for clients and admin.
- To store campaign and video data securely in a database.
- To improve efficiency in digital marketing management.

---

## 🧩 Features

### 👤 Client Module
- Client registration and login
- Request new marketing campaigns
- View campaign approval status
- View advertisement videos uploaded by admin

### 👨‍💼 Admin Module
- Admin login dashboard
- View and approve client campaign requests
- Upload advertisement videos for campaigns
- Manage clients and campaigns
- Delete or update campaign records

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Backend Programming |
| Flask | Web Framework |
| HTML, CSS, JavaScript | Frontend |
| MySQL | Database |
| Bootstrap / Custom CSS | UI Design |
| Font Awesome | Icons |

---

## 🗄️ Database Design

### Main Tables:
- **clients** (client_id, name, email, password)
- **campaigns** (campaign_id, client_id, campaign_name, platform, budget, status)
- **videos** (video_id, campaign_id, video_path, upload_date)
- **admin** (admin_id, username, password)

---

## 📊 System Architecture

### DFD (Data Flow Diagram)
- Level 0 DFD (Context Diagram)
- Level 1 DFD (Detailed Process Flow)

### ERD (Entity Relationship Diagram)
- Client → Campaign (One-to-Many)
- Campaign → Video (One-to-One or One-to-Many)
- Admin manages all entities

---

## 🚀 How to Run the Project

### 1️. Install Required Software
```
- Python 3.x  
- MySQL Server  
- VS Code or any IDE  
```
---

### 2️. Install Python Libraries
```
pip install flask mysql-connector-python
```

---

### 3️. Create Database
```
CREATE DATABASE adindiahub;
```
Import the SQL file provided in the project.


---

### 4️. Run the Project
```
python app.py
```
Open browser and go to:
```
http://127.0.0.1:5000/
```
---

## Advantages

- Reduces manual paperwork

- Centralized campaign management

- Secure data storage

- Easy to use interface

- Time-saving for clients and agency



---

## Limitations

- No online payment integration

- No real-time analytics

- No mobile application

- Manual video creation (no AI generation)

- Limited user roles



---

## Future Enhancements

- AI-based advertisement video generation

- Real-time campaign analytics dashboard

- Mobile application (Android & iOS)

- Social media API integration

- Online payment gateway

- Cloud video storage

- Notification system (Email/SMS)



---

## 👨‍🎓 Developer Details

- **Mahesh Patil :** [![GitHub](https://img.shields.io/badge/@maheshpatil045-%230077B5.svg?logo=github&logoColor=white)](https://github.com/maheshpatil045)
- **Sanket Bhairamadagi :** [![GitHub](https://img.shields.io/badge/@sanketbhairamadagi-%230077B5.svg?logo=github&logoColor=white)](https://github.com/sanketbhairamadagi)

---

## 📜 License

This project is developed for educational purposes only.
