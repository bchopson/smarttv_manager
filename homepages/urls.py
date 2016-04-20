from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(\d+)/$', views.homepage, name='homepage'),
    url(r'^$', views.index, name='index'),
    url(r'^editor/$', views.editor, name='editor'),
    url(r'^readme', views.readme, name='readme')
]