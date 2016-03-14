from django.conf.urls import url

from homepages import views

urlpatterns = [
    url(r'^tvs/$', views.TvList.as_view()),
    url(r'^tvs/(?P<pk>[0-9]+)$', views.TvDetail.as_view()),
    url(r'^tvs/(?P<pk>[0-9]+)/slides/$', views.SlideList.as_view()),
    url(r'^tvs/(?P<pk>[0-9]+)/slides/(?P<idx>[0-9]+)$', views.SlideDetail.as_view()),
]