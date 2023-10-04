from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('<uuid:paste_uuid>/',views.detail,name='detail'),
    path("<slug:short_id>/",views.detail_by_short,name='short-detail'),
]
