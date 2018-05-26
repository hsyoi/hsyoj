from django.db import models


class Record(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    problem = models.ForeignKey(
        "problems.Problem", on_delete=models.SET_NULL, null=True)
    code = models.TextField(editable=False)
    submit_time = models.DateTimeField(auto_now_add=True, editable=False)
    running_time = models.DurationField(editable=False)
