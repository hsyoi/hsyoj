from django.db import models


class Problem(models.Model):
    # Unchangeable Data
    problem_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    hint = models.TextField(blank=True)
    time_limit = models.FloatField(default=1.0)
    memory_limit = models.FloatField(default=256.0)

    # Statistics
    submissions = models.IntegerField(default=0)
    accpected = models.IntegerField(default=0)

    def __str__(self):
        return "{}: {}".format(self.problem_id, self.title)