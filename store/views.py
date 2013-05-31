from django.views.generic import DetailView,ListView
from store.models import Product

class ProductView(DetailView):
	model = Product

class ProductListView(ListView):
	model = Product