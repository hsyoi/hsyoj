from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Record


class Index(generic.ListView):
    template_name = 'records/index.html'
    context_object_name = 'record_list'

    def get_queryset(self):
        return Record.record_set.order_by('submit_time')


@login_required
def detail(request, pk):
    record = get_object_or_404(Record, pk=pk)
    user = request.user
    if user.can_view_record(record):
        return HttpResponse(record)
    return HttpResponse("No Permission.")
