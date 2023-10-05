from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path("register/",views.register,name="register"),
    path("login/",views.login,name="login"),
    path("logout/",views.logout,name="logout"),
    path('<uuid:paste_uuid>/',views.detail,name='detail'),
    path("<slug:short_id>/",views.detail_by_short,name='short-detail'),
]
