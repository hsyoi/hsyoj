from django.urls import path

from . import views

app_name = 'records'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<uuid:pk>/', views.detail, name='detail'),
]
