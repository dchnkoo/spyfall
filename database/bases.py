from .funcs import funcs

import sqlmodel as _sql
import datetime as _date
import typing as _t
import uuid


class PrimaryKey:
    id: uuid.UUID = _sql.Field(default_factory=uuid.uuid4, primary_key=True)


class CreateDate:
    created_date: _date.datetime = _sql.Field(
        sa_type=_sql.DateTime(timezone=True), default_factory=funcs.now_utc
    )


class UpdatedDate:
    updated_date: _t.Optional[_date.datetime] = _sql.Field(
        sa_type=_sql.DateTime(timezone=True),
        sa_column_kwargs={"onupdate": funcs.now_utc},
        default=None,
    )


class Name:
    name: str


class Dates(UpdatedDate, CreateDate): ...
