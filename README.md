# 🛒 E-Commerce Backend API

A production-grade REST API for an e-commerce platform built with **FastAPI** and **MySQL**. Features JWT authentication, role-based access control, cart management, and order processing.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI (Python) |
| Database | MySQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Authentication | JWT (python-jose) |
| Password Hashing | bcrypt (passlib) |
| DB Driver | PyMySQL |
| Validation | Pydantic v2 |
| Environment | python-dotenv |

---

## 📁 Project Structure

```
fastAPI_project/
├── app/
│   ├── main.py               # App entry point
│   ├── database.py           # DB connection & session
│   ├── dependencies.py       # Auth dependencies
│   ├── models/
│   │   ├── user.py           # User, Address models
│   │   ├── product.py        # Product, Category models
│   │   ├── cart.py           # Cart, CartItem models
│   │   └── order.py          # Order, OrderItem models
│   ├── routers/
│   │   ├── auth_routes.py
│   │   ├── product_routes.py
│   │   ├── cart_routes.py
│   │   └── order_routes.py
│   ├── schemas/
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── carts.py
│   │   └── orders.py
│   └── services/
│       ├── auth.py
│       ├── products.py
│       ├── carts.py
│       └── orders.py
├── alembic/                  # DB migrations
├── alembic.ini.example       # Alembic config template
├── .env.example              # Environment variables template
└── requirements.txt
```

---

## ✨ Features

- **JWT Authentication** — Register, login, and secure token-based access
- **Role-Based Access Control** — Admin and User roles with protected routes
- **Product Management** — Full CRUD for products and categories with filters
- **Cart System** — Add, update, remove items with stock validation and price snapshots
- **Order Processing** — Place orders with stock decrement, address snapshot, and status tracking
- **Soft Delete** — Products use `is_active` flag instead of hard deletion
- **Database Migrations** — Full Alembic migration history for all 8 tables

---

## 📡 API Endpoints (25+)

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login with JSON |
| POST | `/auth/login/form` | Login with form data |
| GET | `/auth/me` | Get current user info |

### Products & Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | List products (filters: category, price, stock) |
| POST | `/products` | Create product (Admin) |
| GET | `/products/{id}` | Get product by ID |
| PUT | `/products/{id}` | Update product (Admin) |
| DELETE | `/products/{id}` | Soft delete product (Admin) |
| GET | `/categories` | List all categories |
| POST | `/categories` | Create category (Admin) |
| GET | `/categories/{id}` | Get category by ID |
| PUT | `/categories/{id}` | Update category (Admin) |
| DELETE | `/categories/{id}` | Delete category (Admin) |

### Cart
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cart` | Get cart with total |
| POST | `/cart/items` | Add item to cart |
| PATCH | `/cart/items/{id}` | Update item quantity |
| DELETE | `/cart/items/{id}` | Remove item from cart |
| DELETE | `/cart` | Clear entire cart |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orders` | Place order from cart |
| GET | `/orders/my` | Get my orders |
| GET | `/orders/my/{id}` | Get single order |
| GET | `/orders` | Get all orders (Admin) |
| PATCH | `/orders/{id}/status` | Update order status (Admin) |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- MySQL running locally

### 1. Clone the repository
```bash
git clone https://github.com/srishtis2200/ecommerce-api.git
cd ecommerce-api
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and fill in your values:
```
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/ecommerce_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Configure Alembic
```bash
cp alembic.ini.example alembic.ini
```
Edit `alembic.ini` and update the database URL with your credentials.

### 6. Run database migrations
```bash
alembic upgrade head
```

### 7. Start the development server
```bash
fastapi dev app/main.py
```

### 8. Open API docs
Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

---

## 🗄️ Database Schema

8 tables total:
- `users` — User accounts with role enum (user/admin)
- `addresses` — User delivery addresses with default flag
- `categories` — Product categories
- `products` — Products with stock, price, and soft delete
- `carts` — One cart per user
- `cart_items` — Cart items with price snapshot at time of addition
- `orders` — Orders with status and payment tracking
- `order_items` — Order items with price snapshot at time of purchase

---

## 🔒 Security

- Passwords hashed with **bcrypt**
- Auth via **JWT tokens** (HS256)
- `.env` file excluded from version control
- `alembic.ini` excluded from version control
- Price snapshots prevent price manipulation after order placement

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).