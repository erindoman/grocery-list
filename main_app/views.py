from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, Store
from .forms import PurchaseForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def items_index(request):
    items = Item.objects.filter(user=request.user)
    return render(request, 'items/index.html', { 'items': items })

@login_required
def items_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    stores_item_doesnt_have = Store.objects.exclude(id__in= item.stores.all().values_list('id'))
    purchase_form = PurchaseForm()
    return render(request, 'items/detail.html', { 'item': item, 'purchase_form': purchase_form, 'stores': stores_item_doesnt_have })

@login_required
def add_purchase(request, item_id):
    form = PurchaseForm(request.POST)
    if form.is_valid():
        new_purchase = form.save(commit=False)
        new_purchase.item_id = item_id
        new_purchase.save()
    return redirect('detail', item_id=item_id)

class ItemCreate(CreateView):
    model = Item
    fields = ['name', 'cost', 'quantity']

    def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)

class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['cost', 'quantity']

class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = '/items/'

class StoreList(LoginRequiredMixin, ListView):
  model = Store

class StoreDetail(LoginRequiredMixin, DetailView):
  model = Store

class StoreCreate(LoginRequiredMixin, CreateView):
  model = Store
  fields = '__all__'

class StoreUpdate(LoginRequiredMixin, UpdateView):
  model = Store
  fields = ['name', 'location']

class StoreDelete(LoginRequiredMixin, DeleteView):
  model = Store
  success_url = '/stores/'

def assoc_store(request, item_id, store_id):
    Item.objects.get(id=item_id).stores.add(store_id)
    return redirect('detail', item_id=item_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)