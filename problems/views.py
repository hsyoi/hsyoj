from os import path

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from docutils.core import publish_string

from .models import Problem


class IndexView(generic.ListView):
    template_name = 'problems/index.html'
    context_object_name = 'problem_list'

    def get_queryset(self):
        return Problem.objects.order_by('id')


def detail(request, id):
    problem = get_object_or_404(Problem, pk=id)
    return HttpResponse(
        publish_string(
            source=problem.description,
            writer_name='html'
        )
    )


def records(request, id):
    return HttpResponse("Coming soon!")
