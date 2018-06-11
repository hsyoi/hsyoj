from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse


def index(request):
    return HttpResponse("Coming soon")


@login_required
def detail(request: HttpRequest, pk: int):
    user = request.user
    if user.pk == pk or user.has_perm('user.view_all_users'):
        return HttpResponse(user)
    return HttpResponse("No Permission.")
