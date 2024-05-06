import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Product, Category, Profile
from .forms import SignUpForm, UpdateProfileForm, UpdatePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem

from cart.cart import Cart


def home(request):
    """
    This is the homepage view where you can display all the products, or specific ones you'd like to feature.
    """
    products = Product.objects.all()
    # selected_product = Product.objects.get(pk=1)
    return render(request, 'store/home.html', {'products': products})


# information about app
def about(request):
    """
    This is the about page view where you can describe your service.
    """
    return render(request, 'store/about.html', {})


def login_user(request):
    """
    This is the login page view, it renders the login form and redirects to the home page upon successful login.
    Assumes: login.html; authenticate/login functions from django's authentication framework.
    Cart persistence:
    """
    if request.method == 'POST':  # did the user 'post' the login form
        # get the username and password from the submitted form data
        username = request.POST['username']  # name="username" in login.html template
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  # pass in that data to authenticate user
        if user is not None:
            login(request, user)

            # SHOPPING CART PERSISTENCE UPON LOGIN
            current_user_profile = Profile.objects.get(user__id=request.user.id)
            # get saved cart from database field of 'old_cart'
            current_user_cart = current_user_profile.old_cart
            # convert database string to python dictionary
            if current_user_cart is not None:
                cart_as_dict = json.loads(current_user_cart)
                # now add the cart to session
                cart = Cart(request)
                # loop through cart and add each item to session
                for k, v in cart_as_dict.items():
                    cart.add_from_db(product=k, quantity=v)

            messages.success(request, 'You have been logged in')
            return redirect('home')
        else:
            messages.success(request, 'There was an error, please try again')
            return redirect('login')
    else:
        return render(request, 'store/login.html', {})


def logout_user(request):
    """
    This will log the user out and redirects to the home page upon successful logout.
    Assumes: logout function from django's authentication framework.
    """
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')


def register_user(request):
    """
    This view will render the user registration page and redirects to the user information page upon successful registration.
    The registration form (SignUpForm) was created using django's built in UserCreationForm
    """
    form = SignUpForm()  # define sign up form
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # take all the data that user typed into the form and put it into SignUpForm for use
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered an account, please fill out your billing information')
            return redirect('user-info')
        else:
            messages.success(request, 'There was a problem registering, try again')
            return redirect('register')
    else:
        return render(request, 'store/register.html', {'form': form})
    

# profile view
def user_info(request):
    if request.user.is_authenticated:
        # get current user
        current_user = Profile.objects.get(user__id=request.user.id)  # get profile where its corresponding user id is the current request id
        # get current user's shipping info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # get original user form
        form = UserInfoForm(request.POST or None, instance=current_user)  # when Profile dir is clicked, current information will already be in the form
        # get shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, 'You have updated your profile information')
            return redirect('home')
    else:
        messages.success(request, 'You need to be logged in to access that page')
        return redirect('login')
    
    return render(request, 'store/user_info.html', {'form': form, 'shipping_form': shipping_form})
    

# view for updating user profile
def update_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)  # get current logged-in user and look up in DB
        form = UpdateProfileForm(request.POST or None, instance=current_user)  # when Profile dir is clicked, current information will already be in the form
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, 'You have updated your profile information')
            return redirect('home')
    else:
        messages.success(request, 'You need to be logged in to access that page')
        return redirect('login')

    return render(request, 'store/update_profile.html', {'form': form})


# view for updating password
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # did they fill out the form
        if request.method == 'POST':
            form = UpdatePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                # django automatically logs user out upon updating
                messages.success(request, 'Your password has been updated, please log in again')
                # login(request, current_user) # log them in after they save changes, but right below, redirect back to another page
                return redirect('login')
            else:
                # consider/see if I can use jinja2 templating for errors
                for error in list(form.errors.values()):  # pass in django authentication errors that get thrown
                    messages.error(request, error)
                return redirect('update-password')
        else:
            form = UpdatePasswordForm(current_user)
            return render(request, 'store/update_password.html', {'form': form})
    else:
        messages.success(request, 'You have to be logged in to access this page')
        return redirect('home')


# view for individual product page
def product(request, pk):
    product = Product.objects.get(id=pk)  # query specific product with the primary key from product model
    return render(request, 'store/product.html', {'product': product})


# view for particular category
def category(request, c):
    # handle category names that contain spaces. In the url specifically, spaces are typically replaced with hyphens or
    # underscores to conform to URL encoding standards. However, for the view function, we convert these hyphens back
    # to spaces so that we can accurately look up the category in the database.
    c = c.replace('-', ' ')
    # then we are able to look up the category
    try:
        category = Category.objects.get(name=c)
        products = Product.objects.filter(category=category)
        return render(request, 'store/category.html', {'products': products, 'category': category})
    except:
        messages.success(request, ('That category does not exist'))
        return redirect('home')


# view all categories
def category_summary(request):
    """
    This view will display a page with all the store's categories.
    Remember to manually add each new category name to navbar dropdown menu with the appropriate urls.
    """
    # grab all distinct categories
    categories = Category.objects.all()
    return render(request, 'store/category_summary.html', {'categories': categories})


# product/description search functionality
def search(request):
    # determine if user filled out the form
    if request.method == 'POST':
        search_content = request.POST['searched']  # store/search.html; get the value passed into name="searched"
        # query products, either for name or description
        products = Product.objects.filter(Q(name__icontains=search_content) | Q(description__icontains=search_content))  # icontains; not case-sensitive
        if not products:
            messages.success(request, f'Could not find anything for {search_content}, try again')
            return render(request, 'store/search.html', {})
        else:
            return render(request, 'store/search.html', {'search_content': search_content, 'products': products})
    else:
        return render(request, 'store/search.html', {})
