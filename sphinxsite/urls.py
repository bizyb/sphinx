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
# from django.conf import settings
# from django.conf.urls.static import static
# from django.views.decorators.cache import cache_page

# from django.contrib import admin
# import contact.urls
# import debug_toolbar
# import os
# SERVER_TYPE = os.environ.get('SERVER_TYPE')
# CACHE_LENGTH = 86400 # 24-hour cache expiration

# handle404 = 'views.page_not_found'

# admin.autodiscover()

urlpatterns = [
    url(r'^$', views.apidocs, name='apidocs'),
    url(r'^username-availability$', views.username_availability, name='username-availability'),
    url(r'^invite-code-validation$', views.validate_invite, name='invite-code-validation'),
    # url(r'^$', views.signup, name='signup'),

    
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
