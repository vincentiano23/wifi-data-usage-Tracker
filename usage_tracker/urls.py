from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView
from .views import (
    CustomLoginView,
    dashboard,
    start_session,
    end_session,
    live_data_usage,
    clear_sessions,
)

urlpatterns = [
    path('', dashboard, name='home'),  # Home redirects to dashboard
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('start/', start_session, name='start_session'),
    path('end/<int:session_id>/', end_session, name='end_session'),
    path('live-usage/', live_data_usage, name='live_data_usage'),
    path('clear-sessions/', clear_sessions, name='clear_sessions'),

    # Password change route
    path(
        'change-password/',
        PasswordChangeView.as_view(
            template_name='usage_tracker/password_change_form.html',
            success_url='/dashboard/'
        ),
        name='password_change'
    ),
]
