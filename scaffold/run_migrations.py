from sqlalchemy.dialects.postgresql.named_types import ENUM

from alembic import command
from alembic.config import Config

# The provided scaffold migrations explicitly create PostgreSQL ENUMs
# before creating tables that use those same ENUM objects.
#
# With SQLAlchemy 2.0.30, table creation can attempt to create the ENUM
# a second time. This compatibility shim makes that second operation
# check PostgreSQL first.
_original_on_table_create = ENUM._on_table_create


def _safe_on_table_create(self, target, bind, **kw):
    return self.create(bind=bind, checkfirst=True)


ENUM._on_table_create = _safe_on_table_create


if __name__ == "__main__":
    config = Config("alembic.ini")
    command.upgrade(config, "head")
