from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from HOME.models import Products
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
	cart = Cart(request)
	cart_product = cart.get_products()
	quantities = cart.get_quants
	totals = cart.cart_totals()
	return render(request, "cart_summary.html",
	              {"cart_products": cart_product, "quantities": quantities, 'totals': totals})


def cart_add(request):
	cart = Cart(request)
	if request.method == "POST":
		action = request.POST.get('action')
		if action == 'post':
			product_id = request.POST.get('product_id')
			product_qty = request.POST.get('product_qty')
			try:
				product_id = int(product_id)
				product = get_object_or_404(Products, id=product_id)
				cart.add(product=product, quantity=product_qty)

				cart_quantity = cart.__len__()
				messages.success(request, 'item successfully added in cart.....')
				# return JsonResponse({'Product Name': product.name, 'status': 'success'})
				return JsonResponse({'qty': cart_quantity, 'status': 'success'})
			except ValueError:
				return JsonResponse({"error": "An unexpected error occurred"}, status=500)
			except Exception as e:
				return JsonResponse({"error": "An unexpected error occurred"}, status=500)
		return JsonResponse({"error": "Invalid action"}, status=400)
	return JsonResponse({"error": "Invalid request method"}, status=405)


def cart_update(request):
	cart = Cart(request)
	if request.method == "POST":
		action = request.POST.get('action')
		if action == 'post':
			product_id = request.POST.get('product_id')
			product_qty = request.POST.get('product_qty')
			cart.update(product=product_id, quantity=product_qty)
			messages.success(request, 'item updated successfully.....')
			return JsonResponse({'qty': product_qty, 'status': 'success'})
	return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def cart_delete(request):
	cart = Cart(request)
	if request.method == "POST":
		action = request.POST.get('action')
		if action == 'delete':
			product_id = request.POST.get('product_id')
			cart.delete(product=product_id)
			messages.success(request, 'item deleted successfully.....')
			return JsonResponse({'product': product_id, 'status': 'success'})
		return JsonResponse({'status': 'error', 'message': 'Invalid request'})
