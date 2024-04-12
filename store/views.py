from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Product, Category
from .forms import SignUpForm, UpdateProfileForm, UpdatePasswordForm

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


# information about app
def about(request):
    return render(request, 'store/about.html', {})


# login
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username'] # name="username" in template
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in'))
            return redirect('home')
        else:
            messages.success(request, ('There was an error, please try again'))
            return redirect('login')
    else:
        return render(request, 'store/login.html', {})


# logout
def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out'))
    return redirect('home')


# register
def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST) # take all the data that user typed into the form and put it into SignUpForm for use
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have successfully registered an account'))
            return redirect('home')
        else:
            messages.success(request, ('There was a problem registering, try again'))
            return redirect('register')
    else:
        return render(request, 'store/register.html', {'form': form})
    

# view for updating user profile
def update_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id) # get current logged in user and look up in DB
        form = UpdateProfileForm(request.POST or None, instance=current_user) # when Profile dir is clicked, current information will already be in the form
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, ('You have updated your profile information'))
            return redirect('home')
        
    else:
        messages.success(request, ('You need to be logged in to access that page'))
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
                messages.success(request, ('Your password has been updated, please log in again'))
                # login(request, current_user) # log them in after they save changes, but right below, redirect back to another page
                return redirect('login')
            else:
                # consider/see if i can use jinja2 templating for errors
                for error in list(form.errors.values()): # pass in django authentication errors that get thrown
                    messages.error(request, error)
                return redirect('update-password')
        else:
            form = UpdatePasswordForm(current_user)
            return render(request, 'store/update_password.html', {'form': form})
    else:
        messages.success(request, ('You have to be logged in to access this page'))
        return redirect('home')


# view for individual product page
def product(request, pk):
    product = Product.objects.get(id=pk) # query specific product
    return render(request, 'store/product.html', {'product': product})


# view for particular category
def category(request, c):
    c = c.replace('-', ' ') # replace hyphens in category name spaces in url
    # look up category
    # try:
    category = Category.objects.get(name=c)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category.html', {'products': products, 'category': category})
    # except:
    #     messages.success(request, ('That category does not exist'))
    #     return redirect('home')


# view all categories
def category_summary(request):
    # grab all distinct categories
    categories = Category.objects.all()
    return render(request, 'store/category_summary.html', {'categories': categories})