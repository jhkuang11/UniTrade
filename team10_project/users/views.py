from django.views import generic
from django.db.models import Q
from functools import reduce
from django.contrib.auth.views import login as auth_views_login
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from onlinestore.models import Category, Item

from users.forms import SignUpForm

"""
Views for the users app.

:Date: 2018-11-08
:Authors:
    - Zachary Martin
"""

def signup(request):
        """Handles signup form and keeps category drop down with the page"""
        categories = Category.objects.all()
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                print('valid')
                form.save()
                username = form.cleaned_data.get('username')               
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('/users/login')
        else:
            form = SignUpForm()
        return render(request, 'users/signup.html', {'form': form, 'categories': categories})


def login(*args, **kwargs):
    """Handles login and keeps category drop down with the page"""
    categories = Category.objects.all()
    extra_context = {'categories': categories}
    return auth_views_login(*args, extra_context=extra_context, **kwargs)


class DashboardView(generic.TemplateView):
    """For user dashboard"""
    template_name = "users/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

def approved_items(request, item_id=None):
    if item_id is not None:
        object = Item.objects.get(id=item_id)
        object.delete()
    approved_items = Item.objects.filter(seller=request.user, approved=True).order_by('-create_time')
    categories = Category.objects.all()
    return render(request, 'users/approved_list.html', {'approved_items': approved_items, 'categories': categories})

def pending_items(request, item_id=None):
    if item_id is not None:
        object = Item.objects.get(id=item_id)
        object.delete()
    pending_items = Item.objects.filter(seller=request.user, approved=False).order_by('-create_time')
    categories = Category.objects.all()
    return render(request, 'users/pending_list.html', {'pending_items': pending_items, 'categories': categories})

def delete_pending_item(request, item_id=None):
    try:
        object = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        object = None

    if object is not None:
        object.delete()

    pending_items = Item.objects.filter(seller=request.user, approved=False)
    categories = Category.objects.all()
    return render(request, 'users/pending_list.html', {'pending_items': pending_items, 'categories': categories})

def delete_approved_item(request, item_id=None):
    try:
        object = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        object = None

    if object is not None:
        object.delete()

    approved_items = Item.objects.filter(seller=request.user, approved=True)
    categories = Category.objects.all()
    return render(request, 'users/approved_list.html', {'approved_items': approved_items, 'categories': categories})