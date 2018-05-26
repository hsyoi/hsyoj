from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Problem


class IndexView(generic.ListView):
    template_name = 'problems/index.html'
    context_object_name = 'problem_list'

    def get_queryset(self):
        return Problem.objects.order_by('id')


def detail(request, id):
    with open(f'problems/p/{id}/problem.html') as f:
        return HttpResponse(f.read())


def records(request, id):
    return HttpResponse("Coming soon!")
