from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Item
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
    purchase_form = PurchaseForm()
    return render(request, 'items/detail.html', { 'item': item, 'purchase_form': purchase_form })

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