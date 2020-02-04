from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import User
from equipment.models import Item
from .forms import UserRegisterForm


# Create your views here.
class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")

class UserDetailView(DetailView):
    model = User

@login_required
def profile_view(request, *args, **kwargs):
    obj = Item.objects.filter(db_user=request.user)
    borrowed_context = {
        "object": obj
    }                  
    return render(request, "accounts/user_detail.html", borrowed_context)
