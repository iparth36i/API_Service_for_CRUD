from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout')
]
