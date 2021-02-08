from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as loginUser, update_session_auth_hash
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.urls import reverse
import json
from time import time
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from shoes.settings import *
import razorpay
# client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
# Create your views here.

def home(request):
    shoes = Product.objects.all()
    cats = Category.objects.all()[:7]
    sld = slider.objects.filter(active=True)
    context = {'shoes':shoes, 'cats':cats, 'sld':sld}
    return render(request, 'index.html', context)

def allprod_by_category(request, postslug):
    prod = Product.objects.all().count()
    # cats = Category.objects.filter(slug=postslug)[0]
    catgs = Category.objects.all()
    cat_post = Product.objects.filter(category__slug=postslug)
    context = {'prod':prod,'cat_post':cat_post, 'catgs':catgs}
    return render(request, 'cat-product.html', context)

def prod_details(request, category_slug, slug):
    prod = Product.objects.filter(slug=slug).first()
    category = Product.objects.filter(slug=category_slug)
    catg_parent = Category.objects.all().exclude(parent=True)    
    allcat = Category.objects.all()
    allprod = get_object_or_404(Product, slug=slug)
    #for sizes 
    sz = sizes.objects.filter(shoes=allprod)
    active_size = request.GET.get('size')
    if active_size is None:
        active_size = prod.sizes_set.all().order_by('size').first()
    else:
        active_size = prod.sizes_set.get(size=active_size)
    #for color
    clr = color.objects.filter(shoes=allprod)
    active_clr = request.GET.get('color')
    if active_clr is None:
        active_clr = prod.color_set.all().order_by('image1').first()
    else:
        active_clr = prod.color_set.get(color=active_clr)     
    active_img1 = active_clr.image1
    active_img2 = active_clr.image2
    active_img3 = active_clr.image3
    active_img4 = active_clr.image4
    active_img5 = active_clr.image5
    active_sz = active_size.size
    context = {'prod':prod, 'category':category, 'catg_parent':catg_parent, 'allcat':allcat, 'allprod':allprod, 'sz':sz, 'clr':clr, 'active_color':active_clr,
    'active_img1':active_img1,'active_img2':active_img2,'active_img3':active_img3,'active_img4':active_img4,'active_img5':active_img5, 'active_sizes':active_size}
    return render(request, 'details.html', context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchase=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "This item quantity is updated")
            return redirect("home")
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, "This item is addedd to your cart")
            return redirect("home")
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        print(order)
        messages.info(request, "This item is added to your cart")
        return redirect("home")


# @login_required
# def add_to_cart(request, slug):
#     item = get_object_or_404(Product, slug=slug)
#     # clr = color.objects.filter(shoes=item)
#     # active_clr = request.GET.get('color')
#     order_item = Cart.objects.get_or_create(item=item, user=request.user, purchase=False)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         if order.orderitems.filter(item=item).exists():
#             order_item[0].quantity += 1
#             order_item[0].save()
#             messages.info(request, "This item quantity is updated")
#             return redirect("home")
#         else:
#             order.orderitems.add(order_item[0])
#             messages.info(request, "This item is addedd to your cart")
#             return redirect("home")
#     else:
#         order = Order(user=request.user)
#         order.save()
#         order.orderitems.add(order_item[0])
#         messages.info(request, "This item is added to your cart")
#         return redirect("home")

@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchase=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'cart.html', context={'carts':carts,'order':order})
    else:
        messages.warning(request, "You don't have any item in your cart")
        return redirect("home")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchase=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was removed form your cart")
            return redirect("cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("home")
    else:
        messages.info(request,"You don't have an active order")
        return redirect("home")

@login_required
def increase_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchase=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.title} quantity has been updated")
                return redirect("cart")
            else:
                messages.info(request, f"{item.title} in not in your cart")
                return redirect("home")
        else:
            messages.info(request, "You don't have an active order")
            return redirect("home")

@login_required
def decrease_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchase=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.title} quantity has been updated")
                return redirect("cart")
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.title} item has been removed form your cart")
                return redirect("cart")
        else:
            messages.info(request, "You don't have an active order")
            return redirect("home")


def webadmin(request):
    postcount = Post.objects.all().count()
    catcount = Category.objects.all().count()
    usercount = User.objects.all().count()
    orders = Order.objects.all()
    context = {'postcount':postcount, 'cat':catcount, 'user':usercount,"orders":orders}
    return render(request, 'webadmin/index.html', context)  

def add_post(request):
    posts= PostForm()
    if request.method=='POST':
        posts=PostForm(request.POST, request.FILES)
        if posts.is_valid():
            posts.save()
        messages.success(request, "Posts Added Sucessfully !!")    
        return redirect('allposts')
    return render(request, "webadmin/addpost.html", {'post':posts})

def add_cat(request):
    category= CatForm()
    if request.method=='POST':
        category=CatForm(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addcat.html", {'category':category})

#This is for show all Posts in Custom Admin Panel
def allposts(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'webadmin/allposts.html', context)

#This is for show all Users in Custom Admin Panel
def allusers(request):
    # users = User.objects.all()
    customer = Customer.objects.all()
    context = {
        # 'users':users
    'customer':customer
    }
    return render(request, 'webadmin/allusers.html', context)

def userdetails(request, id):
    customer = Customer.objects.filter(id=id).first()
    context = {'customer':customer}
    return render(request, 'webadmin/user_detail.html', context)

def allorders(request):
    orders = Order.objects.filter(ordered=True)
    carts = Cart.objects.all()
    context = {
    'orders':orders, 'carts':carts,
    }
    return render(request, 'webadmin/allorders.html', context)

#This is for show all Categories in Custom Admin Panel
def allcat(request):
    cat = Category.objects.filter(parent=None).order_by('hit')
    context = {'cat':cat}
    return render(request, 'webadmin/allcat.html', context)

def edit_post(request, id):
    if request.method == 'POST':
        posts = Post.objects.get(id=id)
        editpostForm= EditPostForm(request.POST or None, request.FILES or None, instance=posts)
        if editpostForm.is_valid():
            editpostForm.save()
        messages.success(request, "Post Update Sucessfully !!")
        return redirect('allposts')
    else:
        posts = Post.objects.get(id=id)
        editpostForm= EditPostForm(instance=posts)

    return render(request, "webadmin/editposts.html", {'editpost':editpostForm})
    
def delete_post(request, id):
    delete = Post.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Post Deleted Successfully.")
    return redirect('allposts')


#For edit the categories
def edit_cat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= CatForm(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= CatForm(instance=cat)

    return render(request, "webadmin/editcat.html", {'editcat':editcatForm})

#For delete the categories    
def delete_cat(request, id):
    delete = Category.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Category Deleted Successfully.")
    return redirect('allcat')

# UserSignup Form
def signup(request):
    next_page = request.GET.get('next')
    form=CustomerCreationForm()
    customerForm=CustomerForm()
    mydict={'form':form,'customerForm':customerForm}
    if request.method=='POST':
        form = CustomerCreationForm(request.POST)
        customerForm=CustomerForm(request.POST,request.FILES)
        if form.is_valid() and customerForm.is_valid():
            user = form.save()
            user.email = user.username
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('userlogin')
    context = {'form':form, 'customerForm':customerForm}
    return render(request, 'register.html', context)

# UserSignup Form
def login(request):
    if request.method == 'GET':
        form = Customerloginform() #This comes from forms.py
        next_page = request.GET.get('next') #If url has next value so this function will redirect the user on next page url                
        context = {'form':form}
        return render(request, 'login.html', context)
    else:
        form = Customerloginform(data=request.POST) #This comes from forms.py
        if form.is_valid():
            username = form.cleaned_data.get('username')    
            password = form.cleaned_data.get('password')    
            user = authenticate(username=username, password=password)
            if user:
                loginUser(request, user) #We use loginUser here because yaha 2 login ho gye hai to alag se import kiya hai isko humne
            # messages.success(request, "Welcome Sir")
            #If url has next value so this function will redirect the user on next page url
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:        
                return redirect('home')  
        else:
            context = {'form':form}
            return render(request, 'login.html', context)

def logout(request):
    request.session.clear()
    return redirect('home')
