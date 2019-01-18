from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

# template tagging for relative url
app_name = 'onlinestore'

"""
Routes urls to views in onlinestore app
"""

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),

    url(r'^items/(?P<slug>[-\w]+)/$', views.ListItemView.as_view(), name='item_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.ItemDetailView.as_view(), name='item_detail'),

    url(r'^create_item/$',views.create_item, name='create_item'),
    url(r'^create_item_success/$',views.create_item_success, name='create_item_success'),

    url(r'^privacy/$', views.PrivacyView.as_view(), name='privacy'),

    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^about/xinhuan_qiu$',TemplateView.as_view(template_name="about/xinhuan_qiu.html")),
    url(r'^about/rong_huang$',TemplateView.as_view(template_name="about/rong_huang.html")),
    url(r'^about/jh_kuang$',TemplateView.as_view(template_name="about/jh_kuang.html")),
    url(r'^about/zachary_martin$',TemplateView.as_view(template_name="about/zachary_martin.html")),
    url(r'^about/tolu$',TemplateView.as_view(template_name="about/tolu.html")),
    url(r'^about/mario$',TemplateView.as_view(template_name="about/mario.html")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
