from django.urls import path
from .views import (
    UserDetailView,
    UserCreateView,
    profile_view
)

app_name = 'accounts'
urlpatterns = [
    path('view/<slug:slug>/', profile_view, name='profile-detail') 
]