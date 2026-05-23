from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers.auth_routes import router as auth_router
from app.routers.product_routes import router as product_router
from app.routers.cart_routes import router as cart_router
from app.routers.order_routes import router as order_router

from app.database import engine, Base

# Import ALL models
from app.models.user import User, Address
from app.models.product import Product, Category
from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem

from app.routers.auth_routes import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        with engine.connect() as conn:
            print("✅ MySQL connection successful!")

        # CREATE TABLES
        Base.metadata.create_all(bind=engine)

        print("✅ Tables created successfully!")

    except Exception as e:
        print(f"❌ Startup error: {e}")

    yield

    print("App shutting down...")


app = FastAPI(
    title="E-Commerce API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)

@app.get("/")
def root():
    return {"message": "E-Commerce API is running!"}