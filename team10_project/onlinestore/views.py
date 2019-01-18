from django.views import generic
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Item, Category
from django.shortcuts import render
from functools import reduce
from django import forms
import operator
import re
from .forms import ItemForm
from message.forms import ComposeForm
from onlinestore.forms import ContactForm
from django.views.generic.edit import FormMixin
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from message import views
from message.models import Messages

"""
This file contains views for the onlinestore app.

:Date: 2018-11-13
:Authors:
    - Xinhuan Qiu
    - Mario Marcos
    - Pohung Wang
"""

class HomeView(generic.TemplateView):
    """Class-based view for home page."""
    model = Category
    template_name = "onlinestore/index.html"

    def get_context_data(self, **kwargs):
        """Pass category and item objects to the index template.

        :param kwargs: keyword arguments
        :return: context
        """
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # Only approved items are shown in most recent order
        approved_items = Item.objects.filter(approved=True)
        context['items'] = approved_items.order_by('-create_time')

        # Sorting for index
        context['default_sort'] = "-create_time"
        context['picked_sort'] = self.request.GET.get('sort_value')
        if context['picked_sort'] is None:
            context['items'] = context['items'].order_by(context['default_sort'])
        else:
            context['items'] = context['items'].order_by(context['picked_sort'])

        return context


class ListItemView(generic.ListView):
    """Class-based view for result page."""
    model = Item
    template_name = "item_list.html"

    def get_context_data(self, **kwargs):
        """Pass category and item objects to the item_list/result template.

        :param kwargs: keyword arguments
        :return: context
        """
        context = super(ListItemView, self).get_context_data(**kwargs)
        # pass categories to the template for the drop-down list
        context['categories'] = Category.objects.all()

        # get selection of category from the drop-down list
        category_filter_param = self.kwargs.get('slug')
        context['search_keyword'] = self.request.GET.get('q')


        # if the category param is not a Category object, set it to None
        try:
            category_filter = Category.objects.get(slug=category_filter_param)
        except Category.DoesNotExist:
            category_filter = None

        # initialize sort
        context['default_sort'] = "-create_time"
        context['picked_sort'] = self.request.GET.get('sort_value')

        # check to see if query includes special characters

        context['has_special_characters'] = self.search_string()

        # return items by search if category is none
        if category_filter is None:
            context['items'] = self.get_search_result()
            context['picked_category'] = 'All'
            item_count = self.get_search_result().count()
            if item_count == 0:
                context['suggested_items'] = self.get_suggesteditems()
        else:
            context['items'] = self.get_search_result()
            context['items'] = context['items'].filter(approved=True, category=category_filter)
            context['picked_category'] = category_filter.name
            item_count = context['items'].count()
            if item_count == 0:
                context['suggested_items'] = self.get_suggesteditems()

            context['picked_slug'] = category_filter.slug

        context['num_items'] = context['items'].count()

        if context['num_items'] == 0 and self.get_search_result().count() > 0:
            context['suggested_items_search'] = 1
            context['suggested_items'] = self.get_search_result()


        # sort defaults to recently posted items if not set.
        if context['picked_sort'] is None:
            context['items'] = context['items'].order_by(context['default_sort'])
        else:
            context['items'] = context['items'].order_by(context['picked_sort'])

        return context


    # check to see if search query includes special characters.
    def search_string (self):
        """Searches for special characters, returns None if no special characters found

                :return: the first instance of special character found.
                """
        args = self.request.GET.get('q')
        if (args != None):
            match = re.search('[\x21-\x2F,\x3A-\x40,\x5B-\x60,\x7B-\x7F]', args)
        else:
            match = None
        return match

    # get the item list by search keyword, returns all items if no keyword is passed in
    # def get_queryset(self):

    def get_suggesteditems(self):
        """Get suggested items when search result is none.

        :return: all the items
        """
        suggested_items = super(ListItemView, self).get_queryset().filter(approved=True)
        return suggested_items


    def get_search_result(self):
        """Get items based on the search text.

        :return: items filtered by search text, all items if no text is passed in
        """
        result = super(ListItemView, self).get_queryset().filter(approved=True)
        search_keyword = self.request.GET.get('q')

        # set keyword to None if isspace, will display all the items
        if search_keyword is not None and search_keyword.isspace():
            search_keyword = None

        if search_keyword:
            keyword_list = search_keyword.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in keyword_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in keyword_list))
            )
        return result


class AboutView(generic.TemplateView):
    """Class based view for about page.

    Contains class info and links to team members' pages
    """
    context_object_name = 'about'
    model = Category
    template_name = "about/about.html"

    # pass data to template
    def get_context_data(self, **kwargs):
        """Pass category objects to the about template

        :param kwargs: keyword arguments
        :return: context
        """
        context = super(AboutView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PrivacyView(generic.TemplateView):
    """Class based view for privacy page.

    Contains UniTrade's privacy policies
    """
    context_object_name = 'privacy'
    model = Category
    template_name = "privacy_policy.html"

    # pass data to template
    def get_context_data(self, **kwargs):
        """Pass category objects to the privacy_policy template

        :param kwargs: keyword arguments
        :return: context
        """
        context = super(PrivacyView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ItemDetailView(FormMixin, generic.DetailView):
    """Class based view for item detail page"""
    model = Item
    template_name = "onlinestore/detail.html"
    form_class = ContactForm

    def get_success_url(self):
        return reverse('onlinestore:item_detail', kwargs={'pk': self.object.id})

    # set context for the ListView
    def get_context_data(self, **kwargs):
        """Pass category objects to the detail template

        :param kwargs: keyword arguments
        :return: context
        """
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        # pass categories to the template for the drop-down list
        context['categories'] = Category.objects.all()
        context['form'] = ContactForm

        context['messages_received'] = Messages.objects.filter(item=self.get_object()).order_by('-timestamp')

        return context

    @method_decorator(login_required(login_url='/users/login/'))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.method == "POST":
            form = self.form_class(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.sender = request.user
                post.timestamp = timezone.now()
                messages.success(request, 'Message sent successfully')
                return self.form_valid(post)
            else:
                return self.form_invalid(form)
        else:
            form = self.form_class(initial={'msg': self.request.session['msg']})


    def form_valid(self, form):
        form.save()
        self.request.session['msg'] = form.msg
        return super(ItemDetailView, self).form_valid(form)

    '''Or use this(without attempting session)
    @method_decorator(login_required(login_url='/users/login/'))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            post = form.save(commit=False)
            post.sender = request.user
            post.timestamp = timezone.now()
            messages.success(request, 'Message sent successfully')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        form.save()
        return super(ItemDetailView, self).form_valid(form)
    '''

@login_required(login_url="/users/login/?next={{request.path}}")
def create_item(request):
    """Create item page"""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            try:
                post.seller = request.user
            except Exception as e:
                print(e)
                post.save()
                return redirect('/users/login/?next=/create_item_success/')
            post.save()
            return redirect('/create_item_success/') 
    else:
        form = ItemForm()

    categories = Category.objects.all()
    return render(request, 'onlinestore/create_item.html', {'form': form, 'categories': categories})

def create_item_success(request):
    """Displays success message after user successfully created an item"""
    categories = Category.objects.all()
    return render(request, 'onlinestore/create_item_success.html', {'categories': categories})

