import json

from HOME.models import Products, Profile


class Cart:
	def __init__(self, request):
		self.session = request.session
		self.request = request
		cart = self.session.get('session_key', {})
		if 'session_key' not in request.session:
			cart = self.session['session_key'] = {}
		self.cart = cart

	def db_add(self, product, quantity):
		product_id = str(product)
		product_qty = str(quantity)
		if product_id in self.cart:
			pass
		else:
			self.cart[product_id] = int(product_qty)
		self.session.modified = True
		if self.request.user.is_authenticated:
			current_user = Profile.objects.get(user__id=self.request.user.id)
			current_user.old_cart = json.dumps(self.cart)
			current_user.save()
			print(self.cart)

	def add(self, product, quantity):
		product_id = str(product.id)
		product_qty = str(quantity)
		if product_id in self.cart:
			pass
		else:
			self.cart[product_id] = int(product_qty)

		self.session.modified = True
		if self.request.user.is_authenticated:
			current_user = Profile.objects.get(user__id=self.request.user.id)
			current_user.old_cart = json.dumps(self.cart)  # Convert to valid JSON format
			current_user.save()

	def __len__(self):
		return len(self.cart)

	def cart_totals(self):
		product_ids = self.cart.keys()
		products = Products.objects.filter(id__in=product_ids)
		quantities = self.cart
		total = 0
		for key, value in quantities.items():
			key = int(key)
			for product in products:
				if product.id == key:
					if product.is_sale:
						total = total + (product.sale_price * value)
					else:
						total = total + (product.price * value)
		return total

	def get_products(self):
		product_ids = self.cart.keys()
		products = Products.objects.filter(id__in=product_ids)
		return products

	def get_quants(self):
		quantities = self.cart
		return quantities

	def update(self, product, quantity):
		product_id = str(product)
		product_qty = int(quantity)
		# Get cart
		ourcart = self.cart
		# update Dictionary/cart
		ourcart[product_id] = product_qty
		self.session.modified = True
		thing = self.cart
		if self.request.user.is_authenticated:
			current_user = Profile.objects.filter(user__id=self.request.user.id)
			carty = str(thing)
			current_user.old_cart = json.dumps(carty)
			current_user.update()

		return thing

	def delete(self, product):
		product_id = str(product)
		if product_id in self.cart:
			del self.cart[product_id]
		self.session.modified = True
		if self.request.user.is_authenticated:
			current_user = Profile.objects.filter(user__id=self.request.user.id)
			current_user.old_cart = json.dumps(self.cart)
			current_user.update()
