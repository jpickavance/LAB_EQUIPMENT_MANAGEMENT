from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.urls import reverse_lazy
from accounts.models import User


from .models import Item
from .forms import ItemBookingForm, ItemCreateForm

# Default foreignkey function
def get_default_user():
     return User.objects.get(full_name="ICONAdmin")

# Create your views here.

@login_required
def item_list_view(request, *args, **kwargs):                       #TABLE OF ALL INVENTORY
    obj = Item.objects.order_by('equipment', 'ICON_ref')
    cat = Item.objects.order_by('category').values_list('category', flat = True).distinct()                
    equipment_context = {
        "object": obj,
        "category": cat
    }
    return render(request, "equipment/equipment_list.html", equipment_context)

@login_required
def item_search_view(request, *args, **kwargs):
    query = request.GET.get('category')
    search_all = Item.objects.order_by('ICON_ref').filter(
        category__icontains=query
    )
    search_available = Item.objects.filter(
        category__icontains=query, return_date__iexact=None #this seems to work better than availability
    )
    cat = Item.objects.order_by('category').values_list('category', flat = True).distinct()  
    search_context = {
        "object": search_all,
        "available": search_available,
        "category": cat
        }
    return render(request, "equipment/equipment_search.html", search_context)

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemBookingForm #This ensures equipment.forms.py is called instead of default from model
    success_url = reverse_lazy('equipment:item-list')

    def form_valid(self, form):
        if self.request.user.email == form.data['current_user']:
            form.instance.location = 'storeroom'
            form.instance.current_user = ''
            form.instance.availability = True
            form.instance.return_date = None
            form.instance.borrow_date = None
            form.instance.db_user = get_default_user()
            return super().form_valid(form)
        else:
            form.instance.location = self.request.user.full_name
            form.instance.current_user = self.request.user.email
            form.instance.availability = False
            form.instance.db_user = self.request.user
            return super().form_valid(form)
    

class ItemCreateView(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    model = Item
    form_class = ItemCreateForm
    success_url = reverse_lazy('equipment:item-list')