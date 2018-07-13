from django.db import models


class Problem(models.Model):
    problem_set = models.Manager()

    # Problem's config
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    provider = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, blank=True)

    # testcase_set is auto generated
    input_file_name = models.CharField(max_length=16)
    output_file_name = models.CharField(max_length=16)
    time_limit = models.FloatField(default=1.0)
    memory_limit = models.FloatField(default=256.0)
    stdio_flag = models.BooleanField(default=False)
    optimize_flag = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}: {self.title}"

    def get_problem_config(self) -> dict:
        result = {
            'input_file_name': self.input_file_name,
            'output_file_name': self.output_file_name,
            'test_cases': [
                [tc.input_content, tc.answer_content]
                for tc in self.testcase_set.all()
            ],
            'time_limit': self.time_limit,
            'memory_limit': self.memory_limit,
            'stdio_flag': self.stdio_flag,
            'optimize_flag': self.optimize_flag,
        }
        return result


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_content = models.TextField(blank=False)
    answer_content = models.TextField(blank=False)

    def __str__(self):
        return str(self.pk)
