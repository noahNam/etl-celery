from typing import Type

from sqlalchemy.orm import declarative_base, DeclarativeMeta

datalake_base: Type[DeclarativeMeta] = declarative_base()
warehouse_base: Type[DeclarativeMeta] = declarative_base()
datamart_base: Type[DeclarativeMeta] = declarative_base()
