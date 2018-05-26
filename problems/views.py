from os import path

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import generic
from docutils.core import publish_file

from .models import Problem


class IndexView(generic.ListView):
    template_name = 'problems/index.html'
    context_object_name = 'problem_list'

    def get_queryset(self):
        return Problem.objects.order_by('id')


def detail(request, id):
    problem_rst_file = path.join(
        'problems', 'p', f'{id}', 'problem.rst'
    )
    if path.exists(problem_rst_file):
        return HttpResponse(
            publish_file(
                source=open(problem_rst_file),
                writer_name='html'
            )
        )
    else:
        raise Http404


def records(request, id):
    return HttpResponse("Coming soon!")
