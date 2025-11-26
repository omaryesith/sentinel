from typing import List

from django.shortcuts import get_object_or_404
from domains.models import Domain
from ninja import Router

from .models import PingResult
from .schemas import PingResultSchema
from .services import trigger_manual_check

monitoring_router = Router()


@monitoring_router.post("/{domain_id}/check")
def manual_check(request, domain_id: int):
    """
    Manually triggers a background verification task (Celery).
    Returns the task ID, not the result (because it's asynchronous).
    """
    # Delegate the logic to the service
    result = trigger_manual_check(domain_id)
    return result


@monitoring_router.get("/{domain_id}/history", response=List[PingResultSchema])
def get_domain_history(request, domain_id: int):
    """
    Gets the ping history of a specific domain.
    """
    # Verify that the domain exists
    domain = get_object_or_404(Domain, id=domain_id)

    # Return the results ordered by date (most recent first)
    # Thanks to Ninja and Pydantic, the list of ORM objects is automatically serialized to JSON
    return PingResult.objects.filter(domain=domain)[:50]  # Limit to the last 50
