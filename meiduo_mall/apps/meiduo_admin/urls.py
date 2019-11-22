
from django.conf.urls import url

from .views import admin

urlpatterns = [

    url(r'^authorizations/$', admin.LoginView.as_view())
]
