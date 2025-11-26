from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Domain
from .schemas import DomainIn, DomainOut

domains_router = Router()


@domains_router.post("/", response=DomainOut)
def create_domain(request, payload: DomainIn):
    """Creates a new domain to monitor."""
    domain = Domain.objects.create(**payload.dict())
    return domain


@domains_router.get("/", response=List[DomainOut])
def list_domains(request):
    """Lists all registered domains."""
    return Domain.objects.all()


@domains_router.get("/{domain_id}", response=DomainOut)
def get_domain(request, domain_id: int):
    """Gets the details of a domain."""
    return get_object_or_404(Domain, id=domain_id)
