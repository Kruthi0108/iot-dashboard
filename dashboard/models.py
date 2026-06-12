from django.db import models


class SensorData(models.Model):

    temperature = models.IntegerField()

    humidity = models.IntegerField()

    device_status = models.CharField(
        max_length=10
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Temp: {self.temperature}"