from logging.config import fileConfig
from sqlalchemy import pool, create_engine
from alembic import context
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

load_dotenv()
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import all models
from app.database import Base
from app.models.user import User, Address
from app.models.product import Category, Product
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem

target_metadata = Base.metadata

# Read URL directly from .env — bypasses configparser % issue
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:yourpassword@localhost:3306/ecommerce_db"
)


def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Create engine directly instead of via config (avoids % interpolation bug)
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()