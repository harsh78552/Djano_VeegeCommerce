from .models import Category


def categories(request):
	"""Return all categories to be available in templates."""
	return {'categories': Category.objects.all()}
