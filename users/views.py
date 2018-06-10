from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse


def index(request):
    return HttpResponse("Coming soon")


@login_required
def detail(request: HttpRequest, pk: int):
    user = request.user
    return HttpResponse(f"You are {user.username}.")
