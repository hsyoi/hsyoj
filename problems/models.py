from django.db import models


class Problem(models.Model):
    # Problem's config
    title = models.CharField(max_length=128, unique=True)
    time_limit = models.FloatField(default=1.0)
    memory_limit = models.FloatField(default=256.0)
    description = models.TextField()

    # Statistics
    submissions = models.IntegerField(default=0)
    accpected = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}: {self.title}"


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_content = models.TextField(blank=False)
    answer_content = models.TextField(blank=False)

    def __str__(self):
        return f"{self.problem.title}"
