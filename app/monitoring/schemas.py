from datetime import datetime
from typing import Optional

from ninja import Schema


class PingResultSchema(Schema):
    """
    Defines what the history data looks like when the API returns it.
    """

    id: int
    domain_id: int
    checked_at: datetime
    latency_ms: float
    status_code: int
    is_success: bool
    error_message: Optional[str] = None
