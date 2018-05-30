from django.urls import include, path

app_name = 'users'
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
]
