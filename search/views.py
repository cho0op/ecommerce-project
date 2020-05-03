from django.shortcuts import render
from django.views.generic import ListView
from shop.models import Product


class SearchProductView(ListView):
    queryset = Product.objects.all()
    template_name = 'search/view.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(SearchProductView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query']=query
        return context
    def get_queryset(self):
        request=self.request
        query = request.GET.get('q')
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.none()
