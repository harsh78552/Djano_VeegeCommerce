import json
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Products, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, UpdateUserPasswordForm, UserProfileForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q
from cart.cart import Cart


def search_item(request):
	searched = None
	if request.method == 'POST':
		query = request.POST.get('searched', '').strip()
		if query:
			searched = Products.objects.filter(
				Q(name__icontains=query) or Q(description__icontains=searched))
			if not searched:
				messages.info(request, "That Product does not exist.")
	return render(request, 'search.html', {'searched': searched})


def update_profile(request):
	if request.user.is_authenticated:
		current_users = Profile.objects.get(user__id=request.user.id)
		shipping_users, created = ShippingAddress.objects.get_or_create(user__id=request.user.id)
		form = UserProfileForm(request.POST or None, instance=current_users)
		shipping_form = ShippingForm(request.POST or None, instance=shipping_users)
		if form.is_valid():
			form.save()
			# login(request, current_users)
			messages.success(request, 'Your info successfully updated.....')
			return redirect('home')
		return render(request, 'update_profile.html', {'form': form, 'shipping_form': shipping_form})
	else:
		messages.success(request, 'You must be logged in....')
		return redirect('home')


def update_password(request):
	current_user = request.user
	if request.method == 'POST':
		form = UpdateUserPasswordForm(current_user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'password updated successfully.....')
			login(request, current_user, )
			return redirect('update_user')
		else:
			for error in list(form.errors.values()):
				messages.error(request, error)
	else:
		form = UpdateUserPasswordForm(request.user)
	return render(request, 'update_password.html', {'form': form})


def update_user(request):
	if request.user.is_authenticated:
		current_users = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_users)
		if user_form.is_valid():
			user_form.save()
			login(request, current_users)
			messages.success(request, 'User successfully updated.....')
			return redirect('home')
		return render(request, 'update_user.html', {'user_form': user_form})
	else:
		messages.success(request, 'You must be logged in....')
		return redirect('home')


def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {"categories": categories})


def category(request, sig):
	sig = sig.replace('-', ' ')
	try:
		categories = Category.objects.get(name=sig)
		products = Products.objects.filter(category=categories)
		return render(request, 'category.html', {'products': products, 'category': categories})
	except Category.DoesNotExist:
		messages.error(request, "That category doesn't exist.")
		return redirect('home')


def product(request, pk):
	product = Products.objects.get(id=pk)
	return render(request, "_product_.html", {'product': product})


def home(request):
	products = Products.objects.all()
	categories = Category.objects.all()
	return render(request, "index.html", {'products': products, 'categories': categories})


def about(request):
	return render(request, "about.html", {})


def login_user(request):
	if request.method == 'POST':
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			current_user = Profile.objects.get(user__id=request.user.id)
			saved_cart = current_user.old_cart
			fixed_cart = saved_cart.replace("'", '"')
			print(fixed_cart)
			if saved_cart:
				converted_cart = json.loads(fixed_cart)

				cart = Cart(request)
				for key, value in converted_cart.items():
					cart.db_add(product=key, quantity=value)
			messages.success(request, 'login successfully.....')
			return redirect('home')
		else:
			messages.success(request, 'there was some error....')
			return redirect('login')
	else:
		return render(request, "login.html", {})


def logout_user(request):
	logout(request)
	messages.success(request, 'logged out successfully...')
	return redirect('home')


def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, "Username Created-Please fill out personal info....")
				return redirect('profile_update')
			else:
				messages.error(request, "Authentication failed after registration.")
				return redirect('register')
		else:
			messages.error(request, "User not registered. Check the errors below.")
			print(form.errors)  # Debugging
	return render(request, "register.html", {'form': form})
