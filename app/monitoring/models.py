from django.db import models
from domains.models import Domain


class PingResult(models.Model):
    """
    Stores the result of an individual check.
    It's a basic time series.
    """

    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="pings")
    checked_at = models.DateTimeField(auto_now_add=True)
    latency_ms = models.FloatField(help_text="Response time in milliseconds")
    status_code = models.IntegerField(
        help_text="HTTP status code (e.g.: 200, 404, 500)"
    )
    is_success = models.BooleanField(default=False)

    # Store the error if there was one (e.g.: "Connection Timeout")
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-checked_at"]  # Most recent first
        indexes = [
            models.Index(
                fields=["domain", "-checked_at"]
            ),  # Optimization for charts
        ]

    def __str__(self):
        return f"{self.domain.name} - {self.status_code} ({self.latency_ms}ms)"
