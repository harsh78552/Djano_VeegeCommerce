from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('about/', views.about, name="about"),
	path('login/', views.login_user, name="login"),
	path('logout/', views.logout_user, name="logout"),
	path('update/', views.update_user, name="update"),
	path('update_password/', views.update_password, name="password_update"),
	path('update_profile/', views.update_profile, name="profile_update"),
	path('register/', views.register_user, name="register"),
	path('product/<int:pk>/', views.product, name="product"),
	path('category/<str:sig>/', views.category, name="category"),
	path('category_summary/', views.category_summary, name="category_summary"),
	path('search-item/', views.search_item, name="item-search"),
]
