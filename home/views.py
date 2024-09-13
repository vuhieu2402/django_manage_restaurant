from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Category, Dish, Info
# Create your views here.

class HomePageView(View):
    def get(self, request):
        category_name = request.GET.get('category', 'all')

        categories = Category.objects.all()

        info = Info.objects.first()

        if category_name == 'all':
            dishes = Dish.objects.all()
        else:
            dishes = Dish.objects.filter(category__name__iexact=category_name)

        context = {
            'categories': categories,
            'dishes': dishes,
            'info': info,
            'selected_category': category_name,
        }
        return render(request, 'home/index.html', context)


def menu_view(request):
    category_name = request.GET.get('category', 'all')

    categories = Category.objects.all()

    info = Info.objects.first()

    if category_name == 'all':
        dishes = Dish.objects.all()
    else:
        dishes = Dish.objects.filter(category__name__iexact=category_name)

    context = {
        'categories': categories,
        'dishes': dishes,
        'info': info,
        'selected_category': category_name,
    }
    return render(request, 'home/menu.html', context)



class AboutPageView(View):
    def get(self, request):
        return render(request, 'home/about.html', {})


# class MenuPageView(View):
#     def get(self, request):
#         return render(request, 'home/menu.html', {})

class BookPageView(View):
    def get(self, request):
        return render(request, 'home/book.html', {})

