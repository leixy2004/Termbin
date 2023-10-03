from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('<str:paste_uuid>/',views.detail,name='detail'),
]
