"""
URL configuration for myDjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('blog/', include('blog.urls')),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("img/favicon.ico")),),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('', RedirectView.as_view(url='/blog/home/', permanent=True)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'account.views.custom_page_not_found_view'
handler500 = 'account.views.custom_error_view'
handler403 = 'account.views.custom_permission_denied_view'
handler400 = 'account.views.custom_bad_request_view'
