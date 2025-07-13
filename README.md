# 🗃️ Inventory Management API – Backend CRUD System

This is a fully functional **Inventory Management System backend** built with **Django** and **MySQL**. The system provides complete CRUD operations and follows RESTful best practices.

---

## 🚀 Tech Stack

- **Backend Framework**: Django (with Django REST Framework)
- **Database**: MySQL
- **Testing Tools**:  Django REST Framework’s **Browsable API Interface**
- **Environment**: Python virtual environment (`venv`)

---

## 📁 Project Structure

```
inventory_api/
├── inventory/              # Main Django app
├── inventory_dump.sql             # ✅ Full database schema + sample data
├── requirements.txt        # ✅ All required Python packages
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

4. **Configure your MySQL DB** in `settings.py`:
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

5. **Load the SQL dump**
   ```bash
   mysql -u root -p inventorydb < db_dump.sql
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

---

## ✅ Core Features

- CRUD operations for:
  - 🛍️ **Products**
  - 📂 **Categories**
  - 🧾 **Suppliers**
  - 🔁 **Stock Movements** (auto-updates product quantity)

- Pagination & filtering support in list APIs
- Admin panel with readable model names


---

## 🌟 Creative Add-ons (Standout Features)

### 🔔 1. **Low Stock Alert API**

- 📌 **Endpoint**: `/api/low-stock/`
- 🧠 Lists all products where quantity is **less than 5**
- ✅ Helps businesses track critical stock levels and avoid stockouts
- **Auto-updated** based on stock movements

```json
[
  {
    "id": 3,
    "name": "USB Cable",
    "quantity": 2,
    "status": "LOW STOCK"
  }
]
```

---

### 📊 2. **Category-wise Inventory Stats API**

- 📌 **Endpoint**: `/api/inventory/stats/`
- 📈 Returns total number of products and stock **grouped by category**
- Useful for building dashboards or analytics views

```json
{
  "Electronics": {
    "total_products": 3,
    "total_quantity": 120
  },
  "Groceries": {
    "total_products": 2,
    "total_quantity": 45
  }
}
```

---



## 📮 API Highlights (Sample Routes)

| Method | Endpoint                      | Description                      |
|--------|-------------------------------|----------------------------------|
| GET    | /api/products/                | List all products                |
| POST   | /api/products/                | Create new product               |
| GET    | /api/products/<id>/          | Retrieve product details         |
| PUT    | /api/products/<id>/          | Update product                   |
| DELETE | /api/products/<id>/          | Delete product                   |
| GET    | /api/low-stock/              | List low stock products        |
| GET    | /api/inventory/stats/        | Category-wise inventory stats |

---

## 🧪 Sample Data

- Sample products, categories, suppliers, and movements included in `inventory_dump.sql`
- You can test features like low-stock and stats right away

---

## 👩‍💻 Author

**Surbhi Rana**  
Email: surbhi.rana1803@gmail.com  
GitHub: (https://github.com/ranasurbhi)

---

