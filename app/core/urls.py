from django.contrib import admin
from django.urls import path

# Importamos tus routers
from domains.api import domains_router
from monitoring.api import monitoring_router
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController

# 1. Usamos NinjaExtraAPI para tener soporte de Controladores avanzados
api = NinjaExtraAPI(title="Sentinel Monitoring API", version="1.0.0")

# 2. Registramos el controlador de Auth por defecto
# Esto crea automáticamente rutas como /api/token/pair (Login) y /api/token/refresh
api.register_controllers(NinjaJWTDefaultController)

# 3. Protegemos tus routers existentes
# El argumento auth=JWTAuth() fuerza a que necesites un token para usar estos endpoints
api.add_router("/domains", domains_router, auth=JWTAuth())
api.add_router("/monitoring", monitoring_router, auth=JWTAuth())

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
