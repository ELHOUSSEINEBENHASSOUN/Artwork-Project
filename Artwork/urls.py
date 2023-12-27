from django.urls import path
from .views import *

urlpatterns = [
    path("", signin, name="signin"),
    path("index/", index, name="index"),
    path("create/", create, name="create"),
    path("demande/", demande, name="demande"),
    path('edit/<uuid:id>/', edit, name='edit'),
    path('detail/<uuid:id>/', detail, name='detail'),
    path("signout/", signout, name='signout'),
    path("register/", register, name='register'),
]
