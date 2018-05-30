from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from docutils.core import publish_string

from records.models import Record

from .forms import SubmitForm
from .models import Problem


class IndexView(generic.ListView):
    template_name = 'problems/index.html'
    context_object_name = 'problem_list'

    def get_queryset(self):
        return Problem.problems_set.order_by('pk')


def detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    return HttpResponse(
        publish_string(
            source=problem.description,
            writer_name='html'
        )
    )


def records(request, pk):
    return HttpResponse("Coming soon!")


def submit(request: HttpRequest, pk):
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            # TODO Get user's information ( HOW ??? )
            # user = User.objects.get(pk=user_id)
            # record = Record.generate(
            #     user=user,
            #     problem=Problem.problems_set.get(pk=pk),
            #     **form.cleaned_data
            # )
            # return HttpResponseRedirect(f"records/{record.pk}")
            return HttpResponse("Successed.")
        return HttpResponse("Failed. Please try again.")
    return render(
        request,
        'problems/submit.html',
        {
            'form': SubmitForm(),
            'problem_id': pk,
        }
    )
