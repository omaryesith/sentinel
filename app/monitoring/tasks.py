import logging
import time

import httpx
from celery import shared_task
from django.utils import timezone

from domains.models import Domain

from monitoring.models import PingResult

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def ping_url_task(self, url: str, domain_id: int):
    """
    Performs the asynchronous HTTP ping and saves the result to the database.
    Runs in the 'celery_worker' container.
    """
    logger.info(f"[{domain_id}] Starting ping to: {url}")

    start_time = time.time()
    status_code = 0
    error_msg = None
    is_success = False

    try:
        response = httpx.get(url, timeout=10, follow_redirects=True)
        status_code = response.status_code

        if 200 <= status_code < 400:
            is_success = True
        else:
            error_msg = f"HTTP Error: {status_code}"

    except httpx.RequestError as e:
        error_msg = str(e)
        status_code = 0  # 0 indicates network/connection failure
        is_success = False

    # Calculate latency
    end_time = time.time()
    latency_ms = (end_time - start_time) * 1000

    # --- PERSISTENCE ---
    try:
        domain = Domain.objects.get(id=domain_id)
        
        PingResult.objects.create(
            domain=domain,
            latency_ms=round(latency_ms, 2),
            status_code=status_code,
            is_success=is_success,
            error_message=error_msg,
        )
        logger.info(f"[{domain_id}] Result saved. Status: {status_code}")

    except Domain.DoesNotExist:
        logger.warning(f"Domain {domain_id} not found. Skipping save.")

    return {"domain_id": domain_id, "status": status_code, "latency": latency_ms}


@shared_task
def check_all_domains_task():
    """
    Master task (Cronjob):
    Finds all active domains and dispatches a ping task for each one.
    """
    # Import inside the function to avoid circular references
    from domains.models import Domain

    active_domains = Domain.objects.filter(is_active=True)
    count = 0

    for domain in active_domains:
        ping_url_task.delay(url=domain.url, domain_id=domain.id)
        count += 1

    logger.info(f"Cronjob triggered: {count} ping tasks sent to the queue.")
    return f"Dispatched {count} checks"
