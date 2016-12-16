"""
Url router for the administration site
"""
from django.contrib import admin
from django.conf.urls import url

from views.admin import views as admin_views, ajax as admin_ajax

admin_urls = [

]


urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
