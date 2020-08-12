from django.shortcuts import render


def firework_home(request):
    return render(request, 'fireworks/firework_home.html')


def add_firework(request):
    return render(request, 'fireworks/add_firework.html')


def categories(request):
    return render(request, 'fireworks/categories.html')


def category(request):
    return render(request, 'fireworks/category.html')


def favorites(request):
    return render(request, 'fireworks/favorites.html')


def firework_detail(request):
    return render(request, 'fireworks/firework.html')


def manufacturer(request):
    return render(request, 'fireworks/manufacturer.html')


def manufacturer_category(request):
    return render(request, 'fireworks/manufacturer.html')


def manufacturers(request):
    return render(request, 'fireworks/manufacturers.html')
