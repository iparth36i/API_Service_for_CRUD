from django.urls import path
from .views import *

urlpatterns = [
    path('add/', BoxAddView.as_view(), name='box-add'),
    path('update/<int:pk>/', BoxUpdateView.as_view(), name='box-update'),
    path('list/', BoxListView.as_view(), name='box-list'),
    path('my-boxes/', MyBoxListView.as_view(), name='my-box-list'),
    path('delete/<int:pk>/', BoxDeleteView.as_view(), name='box-delete'),
]
