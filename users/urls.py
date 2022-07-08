from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account, name='account'),
    path('following/', views.following, name='following'),
    path('update-thumbnail/', views.update_thumbnail, name='update-thumbnail'),
    path('save-product/<slug:slug>/', views.save_product, name='save-product'),
    path('saved-products/', views.saved_products, name='saved-products'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html', html_email_template_name='users/html_password_reset_email.html', email_template_name='users/password_reset_email.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/done/',
         auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password-change/',
         auth_views.PasswordChangeView.as_view(
            template_name='users/password_change.html'),
         name='password-change'),
    path('password-change-done/',
         auth_views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('verify-email/', views.verify_email, name='verify-email'),
    path('verify-email/done/', views.verify_email_done, name='verify-email-done'),
    path('verify-email-confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify-email-confirm'),
    path('verify-email/complete/', views.verify_email_complete, name='verify-email-complete'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
]
