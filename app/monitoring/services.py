from django.shortcuts import get_object_or_404
from domains.models import Domain

from .tasks import ping_url_task


def trigger_manual_check(domain_id: int) -> dict:
    """
    Orchestrates the start of a manual check.

    1. Validates that the domain exists.
    2. Dispatches the asynchronous task to Celery.
    3. Returns a confirmation message (not the result, because it's asynchronous).
    """
    domain = get_object_or_404(Domain, id=domain_id)

    domain = get_object_or_404(Domain, id=domain_id)
    task = ping_url_task.delay(url=domain.url, domain_id=domain.id)

    return {
        "message": "Check dispatched successfully",
        "task_id": task.id,
        "domain": domain.name,
    }
