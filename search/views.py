from django.shortcuts import render
from home.models import Dish
# Create your views here.

def search_results(request):
    query = request.GET.get('q')
    if query:
        results = Dish.objects.filter(name__icontains=query)
    else:
        results = Dish.objects.none()
    return render(request, 'search/search_results.html', {'results': results, 'query': query})
