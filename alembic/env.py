"""  
1- add source path by python library ( os, sys) @37
2- import application's configs @39
3- add database url to alembic from config @49
4- import Base class from db.base and models @25
5- config alembic metadata @61
6- re write def run_async_migrations() @104
"""
""" run command:
uv run alembic revision --autogenerate -m "init_users_and_todos"
"""







import sys
import os
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# 4- import Base class from db.base and models
from src.fastapi_learning_project.db.base import Base
import src.fastapi_learning_project.db.models

from alembic import context






#1 add source path by python library ( os, sys)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#2 import application's configs
from src.fastapi_learning_project.core.config import settings





# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
#3 add database url to alembic from config
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# 5- config alembic metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

# 6- re write def run_async_migrations()
async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # >>> this 2 line
    ini_section = config.get_section(config.config_ini_section, {})
    ini_section["sqlalchemy.url"] = str(settings.DATABASE_URL)
    
    
    connectable = async_engine_from_config(
        # >>> and third line
        ini_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
