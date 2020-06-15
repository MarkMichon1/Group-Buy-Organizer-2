from django.shortcuts import render

def home(request):
    context = {
        'title' : 'Home'
    }

    return render(request, 'general/home.html', context=context)


def about(request):
    context = {
        'title' : 'About'
    }

    return render(request, 'general/about.html', context=context)


def updates(request):
    context = {
        'title' : 'Site Updates'
    }

    return render(request, 'general/updates.html', context=context)