import datetime
from django.shortcuts import render
from .models import*
from django.http import JsonResponse
import json


# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_itmes':0,'shipping':False }
        cartItems = order['get_cart_items']
        
    products = Product.objects.all()
    
    return render(request,'store/store.html',{'items':items, 'order': order, 'products':products, 'cartItems':cartItems})

def cart(request):
    context = {}
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_itmes':0,'shipping':False}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    return render(request,'store/cart.html',{'items':items, 'order': order,'products':products, 'cartItems':cartItems})

def checkout(request):
    context = {}
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0,'get_cart_itmes':0.,'shipping':False}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
        
    return render(request,'store/checkout.html',{'items':items, 'order': order,'products':products, 'cartItems':cartItems})
    
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action', action)
    print('productId', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete = False)
    
    orderItem, created= OrderItem.objects.get_or_create(order=order, product=product)
    
    if action =='add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action =='remove':
        orderItem.quantity = (orderItem.quantity-1)
    orderItem.save()
    
    if orderItem.quantity <=0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order, 
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
                
            )
            

    else:
        print("User is Not Logged in..") 
    return JsonResponse("Payment Complete!", safe=False)