from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        permissions = (
            ('view_all_users', "View all users' information."),
        )

    def can_view_record(self, record):
        return record in self.record_set.all() or \
            self.has_perm('record.view_all_records')
