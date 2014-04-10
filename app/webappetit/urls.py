from django.conf.urls import url

from webappetit import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]