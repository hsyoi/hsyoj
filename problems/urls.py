from django.urls import path

from . import views

app_name = 'problems'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:problem_id>/', views.detail, name='detail'),
]
