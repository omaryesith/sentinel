from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from domains.api import domains_router
from monitoring.api import monitoring_router
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController

api = NinjaExtraAPI(title="Sentinel Monitoring API", version="1.0.0")
api.register_controllers(NinjaJWTDefaultController)

api.add_router("/domains", domains_router, auth=JWTAuth())
api.add_router("/monitoring", monitoring_router, auth=JWTAuth())

urlpatterns = [
    path("api/", api.urls),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += [path("admin/", admin.site.urls)]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
