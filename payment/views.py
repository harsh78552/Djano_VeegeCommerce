from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from cart.cart import Cart
from HOME.models import Products, Profile


def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		order = get_object_or_404(Order, id=pk)
		order_item = OrderItem.objects.filter(order=pk)
		if request.method == 'POST':
			status = request.POST.get('shipping_status') == 'true'
			order.shipped = status
			order.save()
			messages.success(request, "Shipping status updated successfully")
			return redirect('home')
		return render(request, 'orders.html', {'order': order, 'order_item': order_item})


def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.method == 'POST':
			status_raw = request.POST.get('shipping_status', '')
			status = request.POST.get('shipping_status') == 'true'
			num = request.POST['num']
			order = Order.objects.filter(id=num)
			order.update(shipped=status)
			messages.success(request, "Shipping status updated successfully")
			return redirect('home')
		return render(request, 'not_shipped_dashboard.html',
		              {'orders': orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')


def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.method == 'POST':
			status = request.POST.get('shipping_status') == 'true'
			num = request.POST['num']
			order = Order.objects.filter(id=num)
			order.update(shipped=status)
			messages.success(request, "Shipping status updated successfully")
			return redirect('home')
		return render(request, 'shipped_dashboard.html',
		              {'orders': orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')


def processor_order(request):
	if request.POST:
		cart = Cart(request)
		cart_products = cart.get_products
		quantities = cart.get_quants()
		totals = [cart.cart_totals()]
		payment_form = PaymentForm(request.POST or None)
		my_shipping = request.session.get('my_shipping')
		full_name = my_shipping.get('shipping_full_name')
		email = my_shipping.get('shipping_email')
		shipping_address = f"{my_shipping.get('shipping_address1')}\n{my_shipping.get('shipping_address2')}\n{my_shipping.get('shipping_city')}\n{my_shipping.get('shipping_state')}\n{my_shipping.get('shipping_zipcode')}\n{my_shipping.get('shipping_country')}"
		amount_paid = totals
		if request.user.is_authenticated:
			user = request.user
			create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address,
			                     amount_paid=amount_paid[0])
			create_order.save()
			order_id = create_order.pk
			for product in cart_products():
				product_id = product.id
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price
					for key, value in quantities.items():
						if int(key) == product.id:
							create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user,
							                              quantity=value, price=price)
							create_order_item.save()
			for key in list(request.session.keys()):
				if key == "session_key":
					del request.session[key]
			current_user = Profile.objects.filter(user__id=request.user.id)
			current_user.update(old_cart="")
			messages.success(request, "Order Placed")
			return redirect('home')


def billing_info(request):
	if request.POST:
		cart = Cart(request)
		cart_products = cart.get_products
		quantities = cart.get_quants()
		totals = [cart.cart_totals()]
		my_shipping = request.POST

		request.session['my_shipping'] = my_shipping
		if request.user.is_authenticated:
			billing_form = PaymentForm()
			return render(request, 'billing_info.html',
			              {'cart_products': cart_products, 'quantities': quantities, 'totals': sum(totals),
			               'shipping_info': request.POST, 'billing_form': billing_form})
		else:
			billing_form = PaymentForm()
			return render(request, 'billing_info.html',
			              {'cart_products': cart_products, 'quantities': quantities, 'totals': sum(totals),
			               'shipping_info': request.POST, 'billing_form': billing_form})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')


def checkout(request):
	cart = Cart(request)
	cart_products = cart.get_products
	quantities = cart.get_quants()
	totals = [cart.cart_totals()]
	if request.user.is_authenticated:
		shipping_users, created = ShippingAddress.objects.get_or_create(user__id=request.user.id)
		shipping_form = ShippingForm(request.POST or None, instance=shipping_users)
		return render(request, 'check_out.html',
		              {'cart_products': cart_products, 'quantities': quantities, 'totals': sum(totals),
		               'shipping_form': shipping_form})
	else:
		shipping_form = ShippingForm(request.POST or None)
		return render(request, 'check_out.html',
		              {'cart_products': cart_products, 'quantities': quantities, 'totals': sum(totals),
		               'shipping_form': shipping_form})


def payment_success(request):
	return render(request, "payment_success.html", {})
