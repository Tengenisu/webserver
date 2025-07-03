# Aryan Vohra Webserver

![Webserver Banner](https://dummyimage.com/1200x300/00d4ff/fff&text=Aryan+Vohra+Webserver)

A modern, full-featured Django webserver for file uploads, folder management, and user authentication with OTP email verification.

---

## 🚀 Features

- **User Registration & Login**
  - Secure registration with OTP email verification
  - Beautiful, modern authentication pages
- **Role-Based Access**
  - Superusers can create, upload, and delete files/folders
  - Normal users can only view and download
- **File & Folder Management**
  - Upload, organize, and preview files
  - Create nested folders
  - Download and preview (including video preview)
- **Responsive UI**
  - Stunning cyan-themed design
  - Mobile-friendly and accessible
- **Admin Panel**
  - Manage users, files, and folders with Django admin

---

## 🛠️ Tech Stack
- **Backend:** Django 5
- **Frontend:** Django Templates, Bootstrap-inspired custom CSS
- **Database:** PostgreSQL (configurable)
- **Email:** Django email backend (console for dev, SMTP for prod)

---

## ⚡ Quick Start

1. **Clone the repo:**
   ```bash
   git clone https://github.com/aryanvohra/webserver.git
   cd webserver
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment:**
   - Copy `.env.example` to `.env` and set your DB/email settings
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the app:**
   - Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## ✨ Screenshots

> _Add your screenshots here!_

---

## 📦 Folder Structure

```
webserver/
├── file_upload/      # File & folder management app
├── user_auth/        # User registration, login, OTP
├── static/           # Static files (CSS, JS, images)
├── templates/        # Base templates
├── webserver/        # Project settings & URLs
└── ...
```

---

## 📝 License

This project is licensed under the [MIT License](LICENSE) — free for personal and commercial use.

---

## 🙏 Acknowledgements
- Django Project
- Bootstrap
- [Choose a License](https://choosealicense.com/)

---

> Made with ❤️ by Aryan Vohra 