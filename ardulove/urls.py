from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

import views, settings

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),

    path('instructions/', include('instructions.urls')),
    path('projects/', include('projects.urls')),
    path('products/', include('products.urls')),
    path('contact/', views.contact_page, name='contact'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
