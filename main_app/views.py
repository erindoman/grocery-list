from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Item, Store
from .forms import PurchaseForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def items_index(request):
    items = Item.objects.all()
    return render(request, 'items/index.html', { 'items': items })

def items_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    stores_item_doesnt_have = Store.objects.exclude(id__in= item.stores.all().values_list('id'))
    purchase_form = PurchaseForm()
    return render(request, 'items/detail.html', { 'item': item, 'purchase_form': purchase_form, 'stores': stores_item_doesnt_have })

def add_purchase(request, item_id):
    form = PurchaseForm(request.POST)
    if form.is_valid():
        new_purchase = form.save(commit=False)
        new_purchase.item_id = item_id
        new_purchase.save()
    return redirect('detail', item_id=item_id)

class ItemCreate(CreateView):
    model = Item
    fields = '__all__'

class ItemUpdate(UpdateView):
    model = Item
    fields = ['cost', 'quantity']

class ItemDelete(DeleteView):
    model = Item
    success_url = '/items/'

class StoreList(ListView):
  model = Store

class StoreDetail(DetailView):
  model = Store

class StoreCreate(CreateView):
  model = Store
  fields = '__all__'

class StoreUpdate(UpdateView):
  model = Store
  fields = ['name', 'location']

class StoreDelete(DeleteView):
  model = Store
  success_url = '/stores/'

def assoc_store(request, item_id, store_id):
    Item.objects.get(id=item_id).stores.add(store_id)
    return redirect('detail', item_id=item_id)