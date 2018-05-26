from django.urls import path

from . import views

app_name = 'problems'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:id>/', views.detail, name='detail'),
    path('<int:id>/records', views.records, name='records'),
]
