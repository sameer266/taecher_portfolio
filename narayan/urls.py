"""
URL configuration for narayan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name="home"),
    
       path('ckeditor/', include('ckeditor_uploader.urls')),
    
    path('subjects/<slug:slug>/', views.subject_detail_view, name='subject_detail'),
    path('notes/<slug:slug>/', views.note_detail_view, name='note_detail'),
    
    path('books/<slug:slug>/', views.book_detail_view, name='book_detail'),
    path('articles/<slug:slug>/', views.article_detail_view, name='article_detail'),
    path('resources/<slug:slug>/', views.course_detail_view, name='course_detail'),
    path('articles/', views.articles_view, name='articles'),
    path('gallery/', views.gallery_list_view, name='gallery'),
    path('blogs/',views.blogs_view,name="blogs"),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),

    
    path('meetup-request/', views.meetup_request_view, name='meetup_request'),
]
       
    
    
    



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)