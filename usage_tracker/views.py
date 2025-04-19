from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash

from .models import UsageSession
from .utils import get_wifi_usage

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')  # Make sure 'login' is the name of your login URL
    else:
        form = UserCreationForm()
    
    return render(request, 'usage_tracker/registration.html', {'form': form})

# Custom login view
class CustomLoginView(LoginView):
    template_name = 'usage_tracker/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')


# Start a new data usage session
@login_required
def start_session(request):
    uploaded, downloaded = get_wifi_usage()
    UsageSession.objects.create(
        user=request.user,
        uploaded_bytes=uploaded,
        downloaded_bytes=downloaded
    )
    messages.success(request, "New session started.")
    return redirect('dashboard')


# End a session and calculate used data
@login_required
def end_session(request, session_id):
    session = get_object_or_404(UsageSession, id=session_id, user=request.user)
    current_uploaded, current_downloaded = get_wifi_usage()

    session.end_time = timezone.now()
    session.uploaded_bytes = max(0, current_uploaded - session.uploaded_bytes)
    session.downloaded_bytes = max(0, current_downloaded - session.downloaded_bytes)
    session.save()

    messages.success(request, "Session ended successfully.")
    return redirect('dashboard')


# Return live data usage as JSON (AJAX-friendly)
@login_required
def live_data_usage(request):
    uploaded, downloaded = get_wifi_usage()
    total_mb = round((uploaded + downloaded) / (1024 * 1024), 2)
    return JsonResponse({
        'uploaded_mb': round(uploaded / (1024 * 1024), 2),
        'downloaded_mb': round(downloaded / (1024 * 1024), 2),
        'total_mb': total_mb
    })


# Clear all sessions for current user
@login_required
def clear_sessions(request):
    UsageSession.objects.filter(user=request.user).delete()
    messages.success(request, "All sessions cleared.")
    return redirect('dashboard')


# Main dashboard view with session history and password form
@login_required
def dashboard(request):
    sessions = UsageSession.objects.filter(user=request.user).order_by('-start_time')
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST' and 'change_password' in request.POST:
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Prevents logout after password change
            messages.success(request, "Your password was updated successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'usage_tracker/dashboard.html', {
    'sessions': sessions,
    'password_change_form': password_form,
})
