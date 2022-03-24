import email
from math import prod
from msilib.schema import ControlEvent
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from .models import *
from .forms import ItemForm
from .forms import UserForm
import json

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User not found!')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist!')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured on during registration - Please try again!')
    context = {'form': form, 'page': page}
    return render(request, 'base/login_register.html', context)


def home(request):

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    items = Item.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(item_name__icontains=q) |
        Q(description__icontains=q)
    )
    clothingTypes = ClothingType.objects.all()
    item_count = items.count()
    context = {'items': items, 'clothes': clothingTypes, 'item_count': item_count, 'cartItems':cartItems}
    return render(request, 'base/home.html', context)

def item(request, pk):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    item_page = None
    items = Item.objects.all()
    for i in items:
        if i.id == int(pk):
            item_page = i
    context = {'item': item_page, 'cartItems':cartItems}
    return render(request, 'base/item.html', context)


#ADD TO CART @login_required(login_url='login')

@login_required(login_url='login')
def createItem(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form, 'cartItems':cartItems}
    return render(request, 'base/item_form.html', context)


@login_required(login_url='login')
def updateItem(request, pk):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
    
    
    item = Item.objects.get(id=pk)
    form = ItemForm(instance=item)
    if request.method == 'POST':
        form = ItemForm(request.POST,  request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form, 'cartItems':cartItems}
    return render(request, 'base/item_form.html', context)



@login_required(login_url='login')
def deleteItem(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': item})

def cart(request):        
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'base/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
        
    if request.method == 'POST':
        print("Hello")
    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'base/checkout.html', context)

def addItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    print('Action: ', action)
    print('ProductID: ', productID)

    customer = request.user
    product = Item.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)