from django.shortcuts import render
from django.shortcuts import redirect
from .models import Category,Product,Cart
from . import models
from .forms import SearchForm
from telebot import TeleBot
# Create your views here.

bot = TeleBot('6244426709:AAEWB5vYxnvX2c3y17uO5EOoZgzRm0ZzvUA', parse_mode='HTML')

def index(request):
    all_products = models.Product.objects.all()
    # Getting from inputed value in search from website
    search_bar = SearchForm()
    all_categories = models.Category.objects.all()

    context = {'all_categories': all_categories,
               'products':all_products,
               'form':search_bar}

    if request.method == "POST":
        product_find = request.POST.get('search_product')
        try:
            search_result = models.Product.objects.get(product_name = product_find)
            return redirect(f'/item/{search_result.id}')
        except:
            return redirect('/')


    return render(request, 'index.html',context)

def current_category(request,pk):
    category = models.Product.objects.get(id = pk)
    context = {'products':category}
    return render(request, 'current_categories.html', context)

def get_exact_category(request,pk):
    exact_category = models.Category.objects.get(id=pk)
    category_products = models.Product.objects.filter(product_category= exact_category)
    return render(request, 'exact_category.html', {'category_products': category_products})

# Get exact product
def get_exact_product(request, pk):

    product = models.Product.objects.get(id=pk)
    context = {'product':product}
    if request.method == 'POST':
        Cart.objects.create(user_id= request.id,
                            user_product = product,
                            user_product_quantity = request.POST.get('user_product_quantity'))
    return redirect('/cart')
    return render(request,'exact_product.html',context)

def get_user_cart(request):
    user_cart = Cart.objects.filter(user_id = request.user.id)
    return render(request,'user_cart.html',{'cart':user_cart})

# Making order
def complete_order(request):
    user_cart = models.Cart.objects.filter(user_id = request.user.id)
    result_message = 'New order (from WebSite)\n\n'
    total_for_all_cart = 0
    for cart in user_cart:
        result_message += f'<b>{cart.user_product} </b> x {cart.user_product_quantity} = {cart.total_for_product}$\n'
        total_for_all_cart += cart.total_for_product
    result_message += f'\n----------\n<b>Total: {total_for_all_cart}$</b>'
    bot.send_message(877993978,result_message)

    return redirect('/')

