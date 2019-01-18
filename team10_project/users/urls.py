from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

app_name = 'users'

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'onlinestore:home'}, name='logout'),

    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^dashboard/approved_items$', views.approved_items, name='approved_items'),
    url(r'^dashboard/pending_items$', views.pending_items, name='pending_items'),
    url(r'^delete_pending/(?P<item_id>[0-9]+)/$', views.delete_pending_item, name='delete_pending'),
    url(r'^delete_approved/(?P<item_id>[0-9]+)/$', views.delete_approved_item, name='delete_approved'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
