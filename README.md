# 🗃️ Inventory Management API – Backend CRUD System

This is a fully functional **Inventory Management System backend** built with **Django** and **MySQL**. The system provides complete CRUD operations and follows RESTful best practices.

---

## 🚀 Tech Stack

- **Backend Framework**: Django (with Django REST Framework)
- **Database**: MySQL
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Testing Tools**: Postman & Django REST Framework’s **Browsable API**
- **Environment**: Python virtual environment (`venv`)

---

## 📁 Project Structure

```
inventory_api/
├── inventory/               # Main Django app
├── inventory_dump.sql       # Full database schema + sample data
├── requirements.txt         # All required Python packages
├── manage.py
└── ...
```

---

## 📦 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd inventory_api
   ```

2. **Create virtual environment & activate**
   ```bash
   python -m venv env
   env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MySQL DB** in `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'inventorydb',
           'USER': 'root',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

5. **Load SQL dump**
   ```bash
   mysql -u root -p inventorydb < inventory_dump.sql
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

---

## ✅ Core Features

- Full CRUD for:
  - 🛍️ **Products**
  - 📂 **Categories**
  - 🧾 **Suppliers**
  - 🔁 **Stock Movements** (auto-updates product quantity)

- 🔍 **Filtering** by category/supplier
- 📑 **Pagination & sorting**
- 🧠 **Search** by product name
- 🛠️ Error handling using try-catch blocks
- ⚙️ Environment-based configuration

---

## 🔐 Advanced Features (Optional for Extra Points)

### 🛡️ JWT-Based Authentication

- ✅ Register/Login endpoints using **JWT tokens**
- 🧾 Protected routes for creating, updating & deleting
- 🔐 Add `Bearer <your-token>` in headers for protected routes

| Method | Endpoint            | Description         |
|--------|---------------------|---------------------|
| POST   | /api/token/         | Get access/refresh token |
| POST   | /api/token/refresh/ | Get new access token |

---

### 🪵 Stock Audit Logging

- 🧾 Every stock IN/OUT movement is logged
- 🔍 API available to view audit logs
- Helps track historical inventory changes

| Method | Endpoint               | Description             |
|--------|------------------------|-------------------------|
| GET    | /api/stock-audit-logs/ | All stock movement logs |

---

### 🔒 Protected Routes Example

- Product create/update/delete only allowed if token is present:
```http
Authorization: Bearer <access_token>
```

---

## 🌟 Creative Add-ons (Standout Features)

### 🔔 1. Low Stock Alert API

- 📌 **Endpoint**: `/api/low-stock/`
- 🚨 Lists products with quantity < 5

### 📊 2. Category-wise Inventory Stats API

- 📌 **Endpoint**: `/api/inventory/stats/`
- 📈 Shows product count & total quantity grouped by category

---

## 📮 API Highlights (Sample Routes)

| Method | Endpoint                      | Description                    |
|--------|-------------------------------|--------------------------------|
| GET    | /api/products/                | List all products              |
| POST   | /api/products/                | Create new product             |
| GET    | /api/products/<id>/          | Retrieve product details       |
| PUT    | /api/products/<id>/          | Update product                 |
| DELETE | /api/products/<id>/          | Delete product                 |
| GET    | /api/low-stock/              | List low stock products        |
| GET    | /api/inventory/stats/        | Category-wise inventory stats  |
| GET    | /api/stock-audit-logs/       | Full audit history of stock    |
| POST   | /api/token/                  | Get JWT access & refresh token |

---

## 🧪 Sample Data

- ✅ All tables prefilled with test data inside `inventory_dump.sql`
- ⚙️ You can test filtering, low-stock alerts, audit logs immediately

---

## 👩‍💻 Author

**Surbhi Rana**  
📧 Email: surbhi.rana1803@gmail.com  
🌐 GitHub: [https://github.com/ranasurbhi](https://github.com/ranasurbhi)