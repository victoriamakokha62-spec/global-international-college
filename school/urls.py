from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('academics/', views.academics, name='academics'),
    path('admissions/', views.admissions, name='admissions'),
    path('news/', views.news, name='news'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('portal/', views.portal, name='portal'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
