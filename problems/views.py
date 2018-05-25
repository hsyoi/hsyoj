from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Problem


def index(request):
    problems = Problem.objects.order_by('problem_id')
    result = '; '.join([
        p.title for p in problems
    ])
    return HttpResponse(result)


def detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return HttpResponse(
        f"This is problem {problem.title}."
    )
