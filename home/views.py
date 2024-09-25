from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from user.views import is_admin
from .models import Category, Dish, Info
from .forms import DishForm



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



@user_passes_test(is_admin, login_url='/login/')
def product_view(request):
    dish = Dish.objects.all()
    category = Category.objects.all()
    return render(request, 'dashboard/product.html', {'dishes': dish, 'categories': category})


@user_passes_test(is_admin, login_url='/login/')
def add_product(request):
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')

    else:
        form = DishForm()

    categories = Category.objects.all()

    return render(request, 'dashboard/add_product.html', {'form': form, 'categories': categories})








