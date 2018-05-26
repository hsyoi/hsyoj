from django.db import models


class User(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=512)
    phone_number = models.DecimalField(max_digits=11, decimal_places=11)
    email = models.EmailField()
    register_time = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.id}: {self.username}"
