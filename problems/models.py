from django.db import models


class Problem(models.Model):
    # Problem's config
    problem_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    time_limit = models.FloatField(default=1.0)
    memory_limit = models.FloatField(default=256.0)

    # Statistics
    submissions = models.IntegerField(default=0)
    accpected = models.IntegerField(default=0)

    def __str__(self):
        return "{}: {}".format(self.problem_id, self.title)
