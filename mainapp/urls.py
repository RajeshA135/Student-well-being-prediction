from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('upload/', views.upload_dataset, name='upload'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('input/', views.input_data, name='input_data'),
    path('result/', views.result, name='result'),
    #path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]




    
