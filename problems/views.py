from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from docutils.core import publish_string

from records.generator import generate_record

from .forms import SubmitForm
from .models import Problem


class IndexView(generic.ListView):
    template_name = 'problems/index.html'
    context_object_name = 'problem_list'

    def get_queryset(self):
        return Problem.problem_set.order_by('pk')


def detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    return HttpResponse(
        publish_string(
            source=problem.description,
            writer_name='html',
        )
    )


def records(request, pk):
    # TODO
    return HttpResponse("Coming soon!")


@login_required
def submit(request: HttpRequest, pk):
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            record = generate_record(
                user=request.user,
                problem=Problem.problem_set.get(pk=pk),
                **form.cleaned_data,
            )
            return HttpResponseRedirect(f"records/{record.pk}")
        return HttpResponse("Failed. Please try again.")
    return render(
        request,
        'problems/submit.html',
        {
            'problem_id': pk,
            'form': SubmitForm(),
        }
    )
