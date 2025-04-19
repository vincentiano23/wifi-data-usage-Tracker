from django.urls import path
from .views import CustomLoginView, dashboard, start_session, end_session, live_data_usage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  
    path('dashboard/', dashboard, name='dashboard'),
    path('start/', start_session, name='start_session'),
    path('end/<int:session_id>/', end_session, name='end_session'),
    path('live-usage/', live_data_usage, name='live_data_usage'),
    path('', dashboard, name='home'),  
]
