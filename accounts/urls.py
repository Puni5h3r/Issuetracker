from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('account_activation_sent/', views.AccountActivationSent.as_view(), name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activated/', views.Activated.as_view(), name='activated'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/newpassword/', views.change_password, name='password_change'),
    path('profile/<uidb64>/<token>/<str:username>/forgotpassword/', views.forgot_password, name='password_forgot'),
    path('accounts/username', views.validate_username, name='validate_username'),

]