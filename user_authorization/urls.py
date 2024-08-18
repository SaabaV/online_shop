# user_authorization/urls.py
from django.urls import path
from user_authorization import views
from user_authorization.views import logout_view

urlpatterns = [
    path('register/', views.registration_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]