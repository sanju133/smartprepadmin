from django.urls import path
from .import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import resend_otp
urlpatterns=[
    path('', views.homepage),
path('resendOTP/', resend_otp),

    path('contact/', views.contact),
	path('card/', views.card),
    path('about/', views.about),
    path('login/', views.login_page),
    path('RegisterForm/', views.register_user),
    path('logout', views.logout_user),
    path('profile/',views.profile),
    # path('registerr', views.register)
path("password-reset/",
    	PasswordResetView.as_view(template_name='user/password_reset.html'),
    	name="password_reset"),

	path("password-reset/done/",
		PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),
		name="password_reset_done"),

	path("password-reset-confirm/<uidb64>/<token>/",
		PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),
		name="password_reset_confirm"),

	path("password-reset-complete/",
		PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
		name="password_reset_complete"),



]