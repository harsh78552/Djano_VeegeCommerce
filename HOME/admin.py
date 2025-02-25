from django.contrib import admin
from django.contrib.auth.models import User

from .models import Category, Products, Customers, Order, Profile

admin.site.register(Category)
admin.site.register(Customers)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(Profile)


class ProfileInline(admin.StackedInline):
	model = Profile


# Extend user  model
class UserAdmin(admin.ModelAdmin):
	model = User
	field = ['username', 'first_name', 'last_name', 'email']
	inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
