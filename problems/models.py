from django.db import models


class Problem(models.Model):
    # Problem's config
    title = models.CharField(max_length=128)
    time_limit = models.FloatField(default=1.0)
    memory_limit = models.FloatField(default=256.0)

    # Statistics
    submissions = models.IntegerField(default=0)
    accpected = models.IntegerField(default=0)

    def __str__(self):
        return "{}: {}".format(self.id, self.title)
