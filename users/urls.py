# users/urls.py
from django.urls import path
from .views import RegisterView, MeView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', MeView.as_view(), name='me'),
    path('', UserListView.as_view(), name='user-list'),

]
