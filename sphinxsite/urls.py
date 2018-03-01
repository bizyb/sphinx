"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.login_view, name='index_login'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'), 
    url(r'^username-availability$', views.username_availability, name='username-availability'),
    url(r'^invite-code-validation$', views.validate_invite, name='invite-code-validation'),
    url(r'^registration$', views.registration, name='registration'),
    url(r'^apidocs$', views.apidocs, name='apidocs'),
    url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
               views.password_reset_view, name='password_reset'),

    
    # url(r'^data-interpretation/$', cache_page(CACHE_LENGTH)(views.data_interpretation), name='interpretation'),
    # url(r'^terms/$', cache_page(CACHE_LENGTH)(views.terms), name='terms'),
    # url(r'^privacy/$', cache_page(CACHE_LENGTH)(views.privacy), name='privacy'),
    # url(r'^reviews/[-\w]+/$', cache_page(CACHE_LENGTH)(views.reviews), name = 'topical_reviews'),
    # url(r'^(?P<slug>[-\w]+)/$', cache_page(CACHE_LENGTH)(views.ArticleDetailView.as_view()), name = 'review'),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]
