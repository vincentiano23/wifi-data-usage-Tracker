from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import UsageSession
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .utils import get_wifi_usage
from django.http import JsonResponse

# Custom login view
class CustomLoginView(LoginView):
    template_name = 'usage_tracker/login.html'
    redirect_authenticated_user = True  
    success_url = reverse_lazy('dashboard')  

# Start a new session
@login_required
def start_session(request):
    uploaded, downloaded = get_wifi_usage()
    session = UsageSession.objects.create(
        user=request.user,
        uploaded_bytes=uploaded,
        downloaded_bytes=downloaded
    )
    return redirect('dashboard')

# End a session safely
@login_required
def end_session(request, session_id):
    session = UsageSession.objects.get(id=session_id, user=request.user)
    current_uploaded, current_downloaded = get_wifi_usage()

    session.end_time = timezone.now()
    session.uploaded_bytes = max(0, current_uploaded - session.uploaded_bytes)
    session.downloaded_bytes = max(0, current_downloaded - session.downloaded_bytes)
    session.save()

    return redirect('dashboard')

@login_required
def live_data_usage(request):
    uploaded, downloaded = get_wifi_usage()
    total_mb = round((uploaded + downloaded) / (1024 * 1024), 2)
    return JsonResponse({
        'uploaded_mb': round(uploaded / (1024 * 1024), 2),
        'downloaded_mb': round(downloaded / (1024 * 1024), 2),
        'total_mb': total_mb
    })
# User dashboard view
@login_required
def dashboard(request):
    sessions = UsageSession.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'usage_tracker/dashboard.html', {'sessions': sessions})
