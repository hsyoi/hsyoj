from django.http import HttpResponse
from django.views import generic

from .models import Record


class Index(generic.ListView):
    template_name = 'records/index.html'
    context_object_name = 'record_list'

    def get_queryset(self):
        return Record.objects.order_by('id')


def detail(request, pk):
    return HttpResponse("Coming soon!")
