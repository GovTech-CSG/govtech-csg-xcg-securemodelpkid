from django.urls import path

from . import views

app_name = "app_name_tests"

urlpatterns = [
    path("", views.test, name="test"),
]
