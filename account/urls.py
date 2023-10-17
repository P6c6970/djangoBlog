from django.urls import path, include
from account import views
from django.contrib.auth import views as auth_views
from .forms import MySetPasswordForm

from utils.for_account import check_recaptcha

urlpatterns = [
    path('register/', check_recaptcha(views.RegisterFormView.as_view()), name="register"),
    path('login/', views.LoginFormView.as_view(), name="_login"),
    path('logout/', views.LogoutView.as_view(), name="_logout"),
    path('profile/id<int:id>/', views.profile, name="profile"),
    path('profile/id<int:id>/follow/', views.ProfileFollowingCreateView.as_view(), name='follow'),
    path('update/', views.UpdateFormView.as_view(), name="update"),
    path('profile/<int:id>/', views.profile),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("password_reset_auth", views.password_reset_request_auth, name="password_reset_auth"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html",
                                                     form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('ban/', views.ban, name="ban"),
]
