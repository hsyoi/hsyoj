from django.db import models


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=512)
    phone_number = models.DecimalField(max_digits=11, decimal_places=11)
    email = models.EmailField()
    register_time = models.DateTimeField()
