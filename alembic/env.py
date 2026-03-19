import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

# Load .env
from dotenv import load_dotenv
load_dotenv()

# Import your models
from app.database import Base
from app import models  # import all models so Alembic sees them

# Alembic Config object
config = context.config

# Use DATABASE_URL from environment variables (works on Render)
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Interpret the config file for logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for Alembic autogenerate
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = db_url or "sqlite:///:memory:"  # fallback URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    if db_url:
        connectable = create_engine(db_url)
        with connectable.connect() as connection:
            context.configure(connection=connection, target_metadata=target_metadata)
            with context.begin_transaction():
                context.run_migrations()
    else:
        # No live DB — skip actual execution
        print("No DATABASE_URL found. Skipping online migrations.")

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()