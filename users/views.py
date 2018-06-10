from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse


def index(request):
    return HttpResponse("Coming soon")


@login_required
def detail(request: HttpRequest, pk: int):
    user = request.user
    if user.pk == pk:
        return HttpResponse(f"You are {user.username}.")
    return HttpResponse("No Permission.")
