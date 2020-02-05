from django.urls import path
from .views import (
    item_list_view,
    ItemCreateView,
    ItemUpdateView
)

app_name = 'equipment'
urlpatterns = [
    path('', item_list_view, name='item-list'),
    path('create/', ItemCreateView.as_view(), name='item-create'),
    path('view/<slug:slug>/book/', ItemUpdateView.as_view(), name='item-book') 
]