from django.urls import path

from . import views

app_name = 'problems'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/records/', views.records, name='records'),
    path('<int:pk>/submit/', views.submit, name='submit'),
]
