# 🛒 Django E-Commerce Store

A fully functional e-commerce web application built using Django.  
This project demonstrates core backend development concepts including authentication, cart management, and session handling.

---

## 🚀 Features

- 🔍 Product search with category filter
- 🛍️ Add to cart without page redirect (UX optimized)
- 🧮 Dynamic cart counter in navbar
- 📦 Order placement system
- 🔐 User authentication (Login/Register/Logout)
- 📄 Order history tracking
- 💬 Flash messages for user feedback
- 📱 Responsive UI using Bootstrap

---

## 🧠 Technical Highlights

- Django session-based cart system
- Context processors for global data (cart count, categories)
- Clean template structure with reusable base layout
- Optimized user experience (reduced navigation friction)
- Modular app structure

---

## 🛠️ Tech Stack

- Python (Django)
- HTML, CSS, Bootstrap
- SQLite (default Django DB)

---

---

## ⚙️ Installation

```bash
git clone https://github.com/ahmadrizwan3611-ux/django-ecommerce

cd django-ecommerce

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
