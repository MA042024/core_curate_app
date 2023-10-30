""" Url router for the curate application
"""
from django.conf.urls import include
from django.urls import re_path


urlpatterns = [
    re_path(r"^", include("core_main_app.urls")),
    re_path(r"^", include("core_curate_app.urls")),
]
