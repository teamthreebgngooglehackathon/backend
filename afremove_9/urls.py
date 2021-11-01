"""afremove_9 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signIn),
    path('postsign/',views.postsign),
    path('logout/', views.logout, name="log"),
    path('signup/',views.signup, name="signup"),
    path('postsignup/',views.postsignup, name="postsignup"),
    path('push_education/',views.push_education, name="pusheducation"),
    path('post_push_education/', views.post_push_education, name="postpusheducation"),
    path('company_submit/',views.company_submit, name="company_submit"),
    path('post_company_submit/',views.post_company_submit, name="post_company_submit"),
    path('createyourprofile/', views.createyourprofile, name="createyourprofile"),
    path('postcreateyourprofile/', views.postcreateyourprofile, name="postcreateyourprofile"),
    path('firebase_upload/', views.firebase_upload, name="firebaseupload"),
    path('postfirebase_upload/', views.postfirebase_upload, name="postfirebase_upload")
]
