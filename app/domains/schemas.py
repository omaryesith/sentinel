from datetime import datetime
from typing import Optional

from ninja import Schema


class DomainIn(Schema):
    name: str
    url: str
    is_active: bool = True


class DomainOut(Schema):
    id: int
    name: str
    url: str
    is_active: bool
    created_at: datetime
