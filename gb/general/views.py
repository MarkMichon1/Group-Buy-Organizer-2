from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, render

from events.models import EventMembership
from general.models import Instance
from general.utilities import app_db_initialization
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from general.mixins import AdminStaffRequiredMixin
from general.models import BlogPost


def home(request):
    memberships = None
    try:
        memberships = EventMembership.objects.filter(user=request.user).order_by('-date_joined')
    except:
        pass
    context = {
        'title_h1_override': True,
        'memberships' : memberships
    }

    return render(request, 'general/home.html', context=context)


def about(request):
    context = {
        'title' : 'About'
    }
    return render(request, 'general/about.html', context=context)


class BlogCreateView(AdminStaffRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'general/blog_create_update.html'
    fields = ['title', 'content']
    success_url = '/updates'
    extra_context = {
        'title' : 'Create New Blog Post'
    }
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BlogDeleteView(AdminStaffRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'general/blog_delete.html'
    success_url = '/updates'
    extra_context = {
        'title': 'Remove Blog?'
    }


class BlogListView(ListView):
    model = BlogPost
    template_name = 'general/updates.html'
    context_object_name = 'blog_posts'
    extra_context = {
        'title': 'Site Updates'
    }
    ordering = ['-date_created']
    paginate_by = 10


class BlogUpdateView(AdminStaffRequiredMixin, UpdateView):
    model = BlogPost
    template_name = 'general/blog_create_update.html'
    fields = ['title', 'content']
    success_url = '/updates'
    extra_context = {
        'title': 'Update Blog Post'
    }

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

def donate(request):
    context = {
        'title': 'Donate'
    }
    return render(request, 'general/donate.html', context=context)


def secret_service_initialization(request):
    instance = Instance.objects.filter(pk=1)
    if instance:
        messages.info(request, 'Already initialized!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        app_db_initialization()
        instance = Instance(service_initialized=True)
        instance.save()
        messages.success(request, 'Initialized!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))