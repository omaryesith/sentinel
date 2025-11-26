from django.core.validators import URLValidator
from django.db import models


class Domain(models.Model):
    """
    Represents a website that we want to monitor.
    """

    name = models.CharField(max_length=255, unique=True)
    url = models.URLField(validators=[URLValidator()], unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.url})"

    class Meta:
        verbose_name = "Domain"
        verbose_name_plural = "Domains"
