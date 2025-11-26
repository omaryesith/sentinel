from django.contrib import admin
from django.urls import path

# Import your routers
from domains.api import domains_router
from monitoring.api import monitoring_router
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController

# 1. Use NinjaExtraAPI to have support for advanced Controllers
api = NinjaExtraAPI(title="Sentinel Monitoring API", version="1.0.0")

# 2. Register the default Auth controller
# This automatically creates routes like /api/token/pair (Login) and /api/token/refresh
api.register_controllers(NinjaJWTDefaultController)

# 3. Protect your existing routers
# The auth=JWTAuth() argument forces the need for a token to use these endpoints
api.add_router("/domains", domains_router, auth=JWTAuth())
api.add_router("/monitoring", monitoring_router, auth=JWTAuth())

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
